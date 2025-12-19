#--------------------------------------------------------------------------------- Location
# myLib/fxcm_api.py

#--------------------------------------------------------------------------------- Description
# fxcm_api

#--------------------------------------------------------------------------------- Import
import inspect, time
import pandas as pd
from myLib.model import model_output
from myLib.logic_global import debug, log_instance, data_instance
from myLib.utils import sort
from myLib.log import Log
from myLib.data_orm import Data_Orm
from myLib.data_sql import Data_SQL
from forexconnect import ForexConnect, fxcorepy

#--------------------------------------------------------------------------------- Action
class Fxcm_API:
    #--------------------------------------------- init
    def __init__(self, account_info:dict, data_orm:Data_Orm=None, data_sql:Data_SQL=None, log:Log=None):
        #--------------------Variable
        self.this_class = self.__class__.__name__
        self.id = account_info.get("username")
        self.name = account_info.get("name")
        self.type = account_info.get("type")
        self.username = account_info.get("username")
        self.password = account_info.get("password")
        self.url = account_info.get("url")
        self.key = account_info.get("key")
        self.fx = ForexConnect()
        #--------------------Instance
        self.data_orm = data_orm if data_orm else data_instance["management_orm"]
        self.data_sql = data_sql if data_sql else data_instance["data_sql"]
        self.log = log if log else log_instance

    #--------------------------------------------- on_status_changed
    def session_status_changed(self, session: fxcorepy.O2GSession, status: fxcorepy.AO2GSessionStatus.O2GSessionStatus):
        print("Trading session status: " + str(status))

    #--------------------------------------------- login
    def login(self):
        #-------------- Description
        # IN     : order_id
        # OUT    : 
        # Action :
        #-------------- Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        start_time = time.time()
        #-------------- Output
        output = model_output()
        output.class_name = self.this_class
        output.method_name = this_method

        try:
            #--------------Action
            result = self.fx.login(self.username, self.password, self.url, self.type, self.session_status_changed)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = result
            output.message = f"{self.name} | {self.type} | {self.id}" 
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 8)} | {sort(this_method, 8)} | {output.time}", output.message)
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
        # IN     : order_id
        # OUT    : 
        # Action :
        #-------------- Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        start_time = time.time()
        #-------------- Output
        output = model_output()
        output.class_name = self.this_class
        output.method_name = this_method

        try:
            #--------------Action
            result = self.fx.logout()
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = result
            output.message= f"{self.type} | {self.id} | {self.name} | {self.balance} | {self.equity}" 
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 8)} | {sort(this_method, 8)} | {output.time}", output.message)
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
    def info(self):
        #-------------- Description
        # IN     : order_id
        # OUT    : 
        # Action :
        #-------------- Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        start_time = time.time()
        #-------------- Output
        output = model_output()
        output.class_name = self.this_class
        output.method_name = this_method

        try:
            #--------------Action
            accounts_table = self.fx.get_table(ForexConnect.ACCOUNTS)
            for account in accounts_table : break
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = account
            output.message= f"{self.name} | {self.id} | Balance: {self.balance} | Equity: {self.equity}"
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 8)} | {sort(this_method, 8)} | {output.time}", output.message)
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
        # IN     : order_id
        # OUT    : 
        # Action :
        #-------------- Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        start_time = time.time()
        #-------------- Output
        output = model_output()
        output.class_name = self.this_class
        output.method_name = this_method

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
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = instruments
            output.message = {"count": len(instruments)}
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 8)} | {sort(this_method, 8)} | {output.time}", output.message)
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
        # IN     : order_id
        # OUT    : 
        # Action :
        #-------------- Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        start_time = time.time()
        #-------------- Output
        output = model_output()
        output.class_name = self.this_class
        output.method_name = this_method
        #-------------- Variable
        attempt = 0
        start = ''
        end = ''
        data_count = 0
        data = None
        
        try:
            #--------------Action
            if dateto > datefrom:
                #-----Get
                while attempt < 3:
                    try: 
                        data = self.fx.get_history(instrument, timeframe, date_from=datefrom, date_to=dateto, quotes_count=count)
                        break
                    except Exception as e:
                        data = None
                        if "No data found" in str(e):
                            break
                        else:
                            self.log.verbose("err", f"{self.this_class} | {this_method}", f"{instrument} | {timeframe} | {datefrom.strftime('%Y-%m-%d %H:%M:%S')} | {dateto.strftime('%Y-%m-%d %H:%M:%S')}")
                            attempt += 1
                            print(f"Error (attempt {attempt}/3): {e}")
                            if attempt > 1: 
                                self.fx.logout()
                                self.fx = ForexConnect()
                                self.fx.login()
                            if attempt >= 3: raise
                            time.sleep(1)
                #-----Check   
                if not data is None: 
                    if data.size>0:
                        df = pd.DataFrame(data)
                        output.data = df
                        start=df["Date"].iloc[0].strftime('%Y-%m-%d %H:%M:%S')
                        end=df["Date"].iloc[-1].strftime('%Y-%m-%d %H:%M:%S')
                        data_count = len(data)
                    else:
                        output.status = False
                else:
                    output.status = False
            else:
                output.status = False
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = data
            output.message =f"{instrument} | {timeframe} | {sort(data_count, 6)} | {start} | {end}"
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 8)} | {sort(this_method, 8)} | {output.time}", output.message)
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

    #--------------------------------------------- orader_open_list
    def orader_open_list(self):
        #-------------- Description
        # IN     : order_id
        # OUT    : 
        # Action :
        #-------------- Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        start_time = time.time()
        #-------------- Output
        output = model_output()
        output.class_name = self.this_class
        output.method_name = this_method
        #--------------Variable
        columns = []
        items = []
        
        try:
            #--------------Data
            data = self.fx.get_table(ForexConnect.TRADES)
            #--------------Column
            for column in data.columns : columns.append(column.id)
            #--------------Items
            for item in data:
                info = {}
                for column in columns : info[column] = getattr(item, column, None)
                items.append(info)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = items
            output.message = len(items)
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 8)} | {sort(this_method, 8)} | {output.time}", output.message)
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

    #--------------------------------------------- orader_close_list
    def orader_close_list(self):
        #-------------- Description
        # IN     : order_id
        # OUT    : 
        # Action :
        #-------------- Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        start_time = time.time()
        #-------------- Output
        output = model_output()
        output.class_name = self.this_class
        output.method_name = this_method
        #--------------Variable
        columns = []
        items = []
        
        try:
            #--------------Data
            data = self.fx.get_table(ForexConnect.CLOSED_TRADES)
            #--------------Column
            for column in data.columns : columns.append(column.id)
            #--------------Items
            for item in data:
                info = {}
                for column in columns : info[column] = getattr(item, column, None)
                items.append(info)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = items
            output.message = len(items)
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 8)} | {sort(this_method, 8)} | {output.time}", output.message)
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
    
    #--------------------------------------------- order_open
    def order_open(self, symbol, action, amount, tp_pips, sl_pips, execute_id):
        #-------------- Description
        # IN     : symbol, action, amount, tp_pips, sl_pips, execute_id
        # OUT    : model_output
        # Action : forex order open
        #-------------- Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        start_time = time.time()
        #-------------- Output
        output = model_output()
        output.class_name = self.this_class
        output.method_name = this_method
        #--------------Variable
        buy_sell = None
        rate=None
        ask = None
        bid = None
        sl = None
        tp = None
                
        try:
            #--------------Check
            amount = int(amount)
            tp_pips = int(tp_pips) 
            sl_pips = int(sl_pips)
            #--------------Data
            command = fxcorepy.Constants.Commands.CREATE_ORDER
            order_type = fxcorepy.Constants.Orders.TRUE_MARKET_OPEN
            buy_sell = fxcorepy.Constants.BUY if action in ("B", "buy") else fxcorepy.Constants.SELL
            #--------------Ask/Bid
            offers = self.fx.get_table(ForexConnect.OFFERS)
            for offer in offers:
                if offer.instrument == symbol:
                    if offer.subscription_status == fxcorepy.Constants.SubscriptionStatuses.TRADABLE:
                        point_size = offer.point_size 
                        digits = offer.digits
                        bid = float(f"{offer.bid:.{digits}f}")
                        ask = float(f"{offer.ask:.{digits}f}")
                        spread = f"{ask-bid:.{digits}f}" 
                        break
            #--------------TP/SL
            if tp_pips or sl_pips:
                if action == "buy":
                    rate = ask
                    tp = float(f"{ask + tp_pips * point_size:.{digits}f}")
                    sl = float(f"{bid - sl_pips * point_size:.{digits}f}")
                elif action == "sell":
                    rate = bid
                    tp = float(f"{bid - tp_pips * point_size:.{digits}f}")
                    sl = float(f"{ask + sl_pips * point_size:.{digits}f}")
            #--------------Order
            if ask and bid :
                if tp or sl:
                    request = self.fx.create_order_request(
                        ACCOUNT_ID=self.api.id,
                        command=command, 
                        order_type=order_type,
                        BUY_SELL= buy_sell,
                        SYMBOL = symbol,
                        AMOUNT= amount,
                        RATE_LIMIT = tp,
                        RATE_STOP = sl
                    )
                else:
                    request = self.fx.create_order_request(
                        ACCOUNT_ID=self.api.id,
                        command=command, 
                        order_type=order_type,
                        BUY_SELL= buy_sell,
                        SYMBOL = symbol,
                        AMOUNT= amount,
                    )
                response = self.fx.send_request(request)
                order_id = getattr(response, "order_id", None) if response else None
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = order_id, bid, ask, tp, sl
            output.message = f"{execute_id} | {order_id} | {symbol} | {action} | {amount} | {rate} | {bid} | {ask} | {tp} | {sl}"
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 8)} | {sort(this_method, 8)} | {output.time}", output.message)
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

    #--------------------------------------------- order_close_all
    def order_close(self, order_ids=None):
        #-------------- Description
        # IN     : order_id
        # OUT    : 
        # Action :
        #-------------- Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        start_time = time.time()
        #-------------- Output
        output = model_output()
        output.class_name = self.this_class
        output.method_name = this_method
        #-------------- Variable
        close_order_ids = []
        
        try:
            #--------------Close
            command = fxcorepy.Constants.Commands.CREATE_ORDER
            order_type = fxcorepy.Constants.Orders.TRUE_MARKET_CLOSE
            items = self.orader_open_list()
            if items.status:
                for item in items.data:
                    order_id = item['open_order_id']
                    trade_id = item['trade_id']
                    symbol = item['instrument']
                    buy_sell = item['buy_sell']
                    amount = item['amount']
                    buy_sell = fxcorepy.Constants.SELL if buy_sell in ("B", "buy") else fxcorepy.Constants.BUY
                    request = self.fx.create_order_request(
                        command=command, 
                        order_type=order_type,
                        ACCOUNT_ID=self.api.id,
                        ORDER_ID=order_id,
                        SYMBOL=symbol,
                        TRADE_ID=trade_id,
                        BUY_SELL= buy_sell,
                        AMOUNT= amount
                    )
                    if order_ids:
                        if order_id in order_ids:
                            self.fx.send_request(request)
                            close_order_ids.append(order_id)
                    else:
                        self.fx.send_request(request)
                        close_order_ids.append(order_id)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = close_order_ids
            output.message =f"{len(items.data)} | {len(order_ids)} | {len(close_order_ids)}"
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 8)} | {sort(this_method, 8)} | {output.time}", output.message)
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