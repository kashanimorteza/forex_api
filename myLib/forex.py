#--------------------------------------------------------------------------------- Location
# myLib/forex.py

#--------------------------------------------------------------------------------- Description
# forex

#--------------------------------------------------------------------------------- Import
import inspect, time
import pandas as pd
from model import model_output
from myLib.forex_api import Forex_Api
from forexconnect import ForexConnect, fxcorepy
from myLib.log import Log
from myLib.database import Database
from myLib.data import Data
from myLib.utils import config, debug, sort, parse_cli_args, format_dict_block, timeframe_nex_date, to_bool


#--------------------------------------------------------------------------------- Action
class Forex:
    #--------------------------------------------- init
    def __init__(self, account):
        #--------------------Variable
        self.this_class = self.__class__.__name__
        self.account = account
        #--------------------Instance
        self.log = Log()
        self.db = Database.instance()
        self.data = Data(log=self.log, db=self.db)
        self.api = Forex_Api(account=account)
        self.fx = self.api.fx

    #--------------------------------------------- run
    def store(self, instrument, timeframe, mode, count, repeat, delay, save, bulk, datefrom, dateto):
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
        #-------------- Action
        try:            
            #---Check
            self.db.open()
            if mode == "up":
                d = self.data.get_max_min(instrument=instrument, timeframe=timeframe, mode="max", filed="Date")
                if d.status and d.data: 
                    datefrom = d.data
                    datefrom = timeframe_nex_date(mode=mode, date=datefrom, timeframe=timeframe)
            elif mode == "down":
                d = self.data.get_max_min(instrument=instrument, timeframe=timeframe, mode="min", filed="Date")
                if d.status and d.data : 
                    dateto = d.data
                    dateto = timeframe_nex_date(mode=mode,date=dateto, timeframe=timeframe)
            #---Display
            params = {"account": self.account,"instrument": instrument, "timeframe": timeframe, "mode": mode, "count": count, "repeat": repeat, "delay": delay, "save": save, "bulk": bulk, "datefrom": datefrom, "dateto": dateto}
            print(format_dict_block("Store", params))
            #---Connection
            self.api.login()
            #---Action
            while(True):
                for r in range(repeat):
                    start = datefrom
                    end = dateto
                    while(True):
                        if end > start:
                            history:model_output = self.history(instrument, timeframe, datefrom=start, dateto=end, count=count)
                            if history.status:
                                if save : self.data.save(instrument=instrument, timeframe=timeframe, data=history.data, bulk=bulk)
                                if mode == "complete" : 
                                    end = timeframe_nex_date(mode ="complete", date=history.data["Date"].iloc[0] , timeframe=timeframe)
                                if mode == "up" : 
                                    start = timeframe_nex_date(mode ="up", date=history.data["Date"].iloc[-1] , timeframe=timeframe)
                                if mode == "down" : 
                                    end = timeframe_nex_date(mode ="down", date=history.data["Date"].iloc[0] , timeframe=timeframe)
                                if mode == "once" : 
                                    break
                            else : break
                            time.sleep(2)
                        else: break
                if delay == 0: break; 
                time.sleep(delay)
            #---Connection
            self.db.close()
            self.api.logout()
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{self.this_class} | {this_method}", output.message)
            #--------------Log
            if log : self.log.log(log_model, output)
            #--------------Output
            return output
        except Exception as e:  
            #--------------Error
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))

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
            output.message["Time"] = sort(int(time.time() - start_time), 3)
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
                symbol = getattr(offer, "symbol", None)
                if instrument_name and symbol : instruments[instrument_name] = symbol
            #--------------Output
            output.data = instruments
            output.message = {
                "Time": sort(int(time.time() - start_time), 3),
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
                        if attempt > 1: 
                            self.fx.logout()
                            forex_api = Forex_Api(account=self.account)
                            self.fx = forex_api.fx
                            forex_api.login()
                            time.sleep(1)
                        if attempt >= 10: raise
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
            output.message = f"{sort(int(time.time() - start_time), 3)} | {instrument} | {timeframe} | {sort(len(data), 6)} | {start} | {end} |"
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
                "Time": sort(int(time.time() - start_time), 3),
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
    def trade_open(self, action, symbol, amount):
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
            if action is "buy" : 
                buy_sell=fxcorepy.Constants.BUY
            elif action=="sell":
                buy_sell=fxcorepy.Constants.SELL
            #--------------Order
            request = self.fx.create_order_request(
                ACCOUNT_ID=self.account["id"],
                command=command, 
                order_type=order_type,
                BUY_SELL= buy_sell,
                SYMBOL = symbol,
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
                "Time": sort(int(time.time() - start_time), 3),
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
    def trade_close(self, order_id, trade_id, symbol, buy_sell, amount):
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
            if buy_sell is "B" : 
                buy_sell=fxcorepy.Constants.SELL
            elif buy_sell=="S":
                buy_sell=fxcorepy.Constants.BUY
            #--------------Request
            request = self.fx.create_order_request(
                command=command, 
                order_type=order_type,
                ACCOUNT_ID=self.account["id"],
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
                "Time": sort(int(time.time() - start_time), 3),
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
                    buy_sell = item['buy_sell']
                    amount = item['amount']
                    self.trade_close(order_id=order_id, trade_id=trade_id, symbol=symbol, buy_sell=buy_sell, amount=amount)
            #--------------Output
            output.message = {
                "Time": sort(int(time.time() - start_time), 3),
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