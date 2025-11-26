#--------------------------------------------------------------------------------- Location
# myLib/forex.py

#--------------------------------------------------------------------------------- Description
# forex

#--------------------------------------------------------------------------------- Import
import inspect, time
import pandas as pd
import utils as utils
from model import model_output
from log import Log
from debug import debug
from utils import config
from forexconnect import ForexConnect, fxcorepy

#--------------------------------------------------------------------------------- Action
class Forex:
    #--------------------------------------------- init
    def __init__(self, log:Log=None, account=None):
        #--------------------Variable
        self.this_class = self.__class__.__name__
        #--------------------Instance
        self.log = Log() if log is None else log
        self.fx = ForexConnect()
        #--------------------Data
        self.account = account
        self.info = None
        self.server = config['forex_connect'][account]['server']
        self.username = config['forex_connect'][account]['username']
        self.password = config['forex_connect'][account]['password']
        self.url = config['forex_connect'][account]['url']
        self.key = config['forex_connect'][account]['key']

    #--------------------------------------------- on_status_changed
    def session_status_changed(self, session: fxcorepy.O2GSession, status: fxcorepy.AO2GSessionStatus.O2GSessionStatus):
        print("Trading session status: " + str(status))

    #--------------------------------------------- login
    def login(self):
        #-------------- Description
        # IN     : 
        # OUT    : 
        # Action :
        #-------------- Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        output = model_output()
        start_time = time.time()

        try:
            #--------------Action
            if verbose : self.log.verbose("rep", f"{self.this_class} | {this_method}", f"Trying to connect({self.account})...")
            self.fx.login(self.username, self.password, self.url, self.server, self.session_status_changed)
            #--------------Output
            output.message = {
                "Time": utils.sort(int(time.time() - start_time), 3),
                "account": self.account,
            }
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{self.this_class} | {this_method}", output.message)
            #--------------Log
            if log : self.log.log(log_model, output)
        except Exception as e:  
            #--------------Error
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Return
        return output

    #--------------------------------------------- logout
    def logout(self):
        #-------------- Description
        # IN     : 
        # OUT    : 
        # Action :
        #-------------- Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        output = model_output()
        start_time = time.time()
        #--------------Action
        try:
            self.fx.logout()
            #--------------Output
            output.message = {
                "Time": utils.sort(int(time.time() - start_time), 3),
                "account": self.account,
            }
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{self.this_class} | {this_method}", output.message)
            #--------------Log
            if log : self.log.log(log_model, output)
        except Exception as e:  
            #--------------Error
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Return
        return output
    
    #--------------------------------------------- instruments
    def instruments(self):
        #-------------- Description
        # IN     : 
        # OUT    : output object with instruments dictionary
        # Action : Get all available instruments with their offer IDs
        #-------------- Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        output = model_output()
        start_time = time.time()

        try:
            #--------------Variable
            offers_table = self.fx.get_table(ForexConnect.OFFERS)
            instruments = {}
            #--------------Action
            for offer in offers_table:
                instrument_name = getattr(offer, "instrument", None) or getattr(offer, "symbol", None)
                offer_id = getattr(offer, "offer_id", None)
                if instrument_name and offer_id : instruments[instrument_name] = offer_id
            #--------------Output
            output.data = instruments
            output.message = {
                "Time": utils.sort(int(time.time() - start_time), 3),
                "count": len(instruments)
            }
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{self.this_class} | {this_method}", output.message)
            #--------------Log
            if log : self.log.log(log_model, output)
        except Exception as e:  
            #--------------Error
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Return
        return output 

    #--------------------------------------------- history
    def history(self, instrument, timeframe, datefrom=None, dateto=None, count=None):
        #-------------- Description
        # IN     : 
        # OUT    : 
        # Action :
        #-------------- Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        output = model_output()
        start_time = time.time()
        #-------------- Variable
        attempt = 0
        start = ''
        end = ''
        #--------------Action
        try:
            if dateto > datefrom:
                #-----Get
                while attempt < 10:
                    try: 
                        data = self.fx.get_history(instrument, timeframe, date_from=datefrom, date_to=dateto, quotes_count=count)
                        break
                    except Exception as e:
                        self.log.verbose("err", f"{self.this_class} | {this_method}", f"{instrument} | {timeframe} | {datefrom.strftime('%Y-%m-%d %H:%M:%S')} | {dateto.strftime('%Y-%m-%d %H:%M:%S')}")
                        attempt += 1
                        print(f"Error (attempt {attempt}/10): {e}")
                        if attempt >= 10:
                            raise
                        time.sleep(1)
                #-----Check
                if len(data)>0:
                    df = pd.DataFrame(data)
                    output.data = df
                    start=df["Date"].iloc[0].strftime('%Y-%m-%d %H:%M:%S')
                    end=df["Date"].iloc[-1].strftime('%Y-%m-%d %H:%M:%S')
                else:
                    output.status = False
            else:
                output.status = False
            output.message = f"{utils.sort(int(time.time() - start_time), 3)} | {instrument} | {timeframe} | {utils.sort(len(data), 6)} | {start} | {end} |"
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{self.this_class} | {this_method}", output.message)
            #--------------Log
            if log : self.log.log(log_model, output)
        except Exception as e:  
            #--------------Error
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Return
        return output

    #--------------------------------------------- account_info
    def account_info(self):
        #-------------- Description
        # IN     : 
        # OUT    : 
        # Action :
        #-------------- Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        output = model_output()
        start_time = time.time()

        try:
            #-------------- Variable
            accounts_table = self.fx.get_table(ForexConnect.ACCOUNTS)
            #--------------Action
            for account in accounts_table:
                output.data["id"] = account.account_id
                output.data["name"] = account.account_name
                output.data["balance"] = account.balance
                output.data["equity"] = account.equity
                break
            #--------------Output
            output.message["Time"] = utils.sort(int(time.time() - start_time), 3)
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{self.this_class} | {this_method}", output.message)
            #--------------Log
            if log : self.log.log(log_model, output)
        except Exception as e:  
            #--------------Error
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Return
        return output
    
    #--------------------------------------------- trade_list
    def trade_list(self):
        #-------------- Description
        # IN     : 
        # OUT    :
        # Action : Get all trade
        #-------------- Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        output = model_output()
        start_time = time.time()
        
        try:
            #--------------Variable
            columns = []
            items = []
            data = self.fx.get_table(ForexConnect.TRADES)
            #--------------Column
            for column in data.columns : columns.append(column.id)
            #--------------Items
            for item in data:
                info = {}
                for column in columns : info[column] = getattr(item, column, None)
                items.append(info)
            #--------------Output
            output.data = items
            output.message = {
                "Time": utils.sort(int(time.time() - start_time), 3),
                "count": len(items),
            }
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{self.this_class} | {this_method}", output.message)
            #--------------Log
            if log : self.log.log(log_model, output)
        except Exception as e:  
            #--------------Error
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Return
        return output
    
    #--------------------------------------------- trade_open
    def trade_open(self, symbol, buy_sell, amount):
        #-------------- Description
        # IN     : 
        # OUT    : 
        # Action :
        #-------------- Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        output = model_output()
        start_time = time.time()
        
        try:
            #--------------Variable
            command = fxcorepy.Constants.Commands.CREATE_ORDER
            order_type = fxcorepy.Constants.Orders.TRUE_MARKET_OPEN
            #--------------Order
            request = self.fx.create_order_request(
                command=command, 
                order_type=order_type,
                ACCOUNT_ID=self.info["id"],
                BUY_SELL= buy_sell,
                SYMBOL= symbol,
                AMOUNT= amount
            )
            response = self.fx.send_request(request)
            response_details = {
                "order_id": getattr(response, "order_id", None) if response else None,
                "trade_id": getattr(response, "trade_id", None) if response else None,
                "symbol": symbol,
                "buy_sell": buy_sell,
                "amount": amount
            }
            #--------------Output
            output.data = response_details
            output.message = {
                "Time": utils.sort(int(time.time() - start_time), 3),
                "Items": f"{symbol} | {buy_sell} | {amount}",
            }
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{self.this_class} | {this_method}", output.message)
            #--------------Log
            if log : self.log.log(log_model, output)
        except Exception as e:  
            #--------------Error
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Return
        return output

    #--------------------------------------------- trade_close
    def trade_close(self, order_id, symbol, trade_id, buy_sell, amount):
        #-------------- Description
        # IN     : 
        # OUT    : 
        # Action :
        #-------------- Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        output = model_output()
        start_time = time.time()
        
        try:
            #--------------Variable
            command = fxcorepy.Constants.Commands.CREATE_ORDER
            order_type = fxcorepy.Constants.Orders.TRUE_MARKET_CLOSE
            #--------------Request
            request = self.fx.create_order_request(
                command=command, 
                order_type=order_type,
                ACCOUNT_ID=self.info["id"],
                ORDER_ID=order_id,
                SYMBOL=symbol,
                TRADE_ID=trade_id,
                BUY_SELL= buy_sell,
                AMOUNT= amount
            )
            response = self.fx.send_request(request)
            response_details = {
                "request_id": request.request_id,
                "response_type": getattr(response, "type", None) if response else None,
                "order_id": getattr(response, "order_id", None) if response else None,
            }
            #--------------Output
            output.data = response_details["order_id"]
            output.message = {
                "Time": utils.sort(int(time.time() - start_time), 3),
                "Items": f"{order_id} | {symbol} | {trade_id} | {buy_sell} | {amount}",
            }
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{self.this_class} | {this_method}", output.message)
            #--------------Log
            if log : self.log.log(log_model, output)
        except Exception as e:  
            #--------------Error
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Return
        return output

    #--------------------------------------------- trade_close
    def trade_close_all(self):
        #-------------- Description
        # IN     : 
        # OUT    : 
        # Action :
        #-------------- Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        output = model_output()
        start_time = time.time()
        
        try:
            #--------------Variable
            items = self.trade_list()
            #--------------Action
            if items.status:
                for item in items.data:
                    order_id = item['open_order_id']
                    trade_id = item['trade_id']
                    symbol = item['instrument']
                    buy_sell = "B" if item['buy_sell'] == "S" else "S"
                    amount = item['amount']
                    self.trade_close(order_id=order_id, symbol=symbol, trade_id=trade_id, buy_sell=buy_sell, amount=amount)
            #--------------Output
            output.message = {
                "Time": utils.sort(int(time.time() - start_time), 3),
                "Items": len(items.data),
            }
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{self.this_class} | {this_method}", output.message)
            #--------------Log
            if log : self.log.log(log_model, output)
        except Exception as e:  
            #--------------Error
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Return
        return output