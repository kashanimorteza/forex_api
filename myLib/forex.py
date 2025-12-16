#--------------------------------------------------------------------------------- Location
# myLib/forex.py

#--------------------------------------------------------------------------------- Description
# forex

#--------------------------------------------------------------------------------- Import
import inspect, time
from datetime import timedelta
import pandas as pd
from myLib.model import model_output
from myLib.logic_global import config, debug, log_instance, data_instance
from myLib.utils import sort, get_tbl_name, format_dict_block
from myLib.log import Log
from myLib.data_orm import Data_Orm
from myLib.data_sql import Data_SQL
from myLib.forex_api import Forex_Api
from forexconnect import ForexConnect, fxcorepy
from myModel import *

#--------------------------------------------------------------------------------- Action
class Forex:
    #--------------------------------------------- init
    def __init__(self,
            forex_api:Forex_Api,
            data_orm:Data_Orm=None,
            data_sql:Data_SQL=None,
            log:Log=None
        ):
        #--------------------Variable
        self.this_class = self.__class__.__name__
        self.api = forex_api
        self.fx:ForexConnect = self.api.fx
        #--------------------Instance
        self.data_orm = data_orm if data_orm else data_instance["management_orm"]
        self.data_sql = data_sql if data_sql else data_instance["data_sql"]
        self.log = log if log else log_instance

    #--------------------------------------------- timeframe_nex_date
    def timeframe_nex_date(self, timeframe, date):
        #-------------- Description
        # IN     : 
        # OUT    : 
        # Action :
        #-------------- Data
        timeframe = timeframe.lower()
        #--------------Action
        if timeframe == "w1" : date = (date - timedelta(days=7))
        elif timeframe == "d1" : date = (date - timedelta(days=1))
        elif timeframe == "h8": date = (date - timedelta(hours=8))
        elif timeframe == "h6": date = (date - timedelta(hours=6))
        elif timeframe == "h4": date = (date - timedelta(hours=4))
        elif timeframe == "h3": date = (date - timedelta(hours=3))
        elif timeframe == "h2": date = (date - timedelta(hours=4))
        elif timeframe == "h1": date = (date - timedelta(hours=1))
        elif timeframe == "m30": date = (date - timedelta(minutes=30))
        elif timeframe == "m15": date = (date - timedelta(minutes=15))
        elif timeframe == "m5": date = (date - timedelta(minutes=5))
        elif timeframe == "m1": date = (date - timedelta(minutes=1))
        elif timeframe == "t1": date = (date - timedelta(milliseconds=1))
        #--------------Output
        return date

    #-------------------------- [get_max_min]
    def get_max_min(self, instrument, timeframe, mode, filed) -> model_output:
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
            #-------------- Data
            tblName = get_tbl_name(instrument, timeframe)
            if mode == "max" : query = f"SELECT max({filed}) FROM {tblName}"
            if mode == "min" : query = f"SELECT min({filed}) FROM {tblName}"
            #--------------Action
            result = self.data_sql.db.item(query)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = result.data
            output.message=f"{instrument} | {timeframe} | {mode} | {filed}"
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

    #-------------------------- [save]
    def save(self, instrument, timeframe, data, bulk=False) -> model_output:
        #-------------- Description
        # IN     : 
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
        start_time = time.time()
        iter = 0 
        insert = 0

        try:
            #-------------- Data
            tblName = get_tbl_name(instrument, timeframe)
            if timeframe == "t1" : query = f'INSERT INTO {tblName} (date, bid, ask) VALUES '
            if timeframe != "t1" : query = f'INSERT INTO {tblName} (date, bidopen, bidclose, bidhigh, bidlow, askopen, askclose, askhigh, asklow) VALUES '
            #--------------Action
            if timeframe == "t1":
                if bulk :
                    data = data.drop_duplicates(subset=["Date"], keep="first")
                    for index, row in data.iloc[::-1].iterrows(): 
                        iter += 1
                        insert += 1
                        query += f"('{row['Date']}',{row['Bid']},{row['Ask']}),"
                    if iter > 0 : query = query[:-1]
                    result = self.data_sql.db.execute(query)
                    if not result.status : insert = 0
                else:
                    for index, row in data.iloc[::-1].iterrows():
                        iter += 1
                        q = query + (f"('{row['Date']}',{row['Bid']},{row['Ask']})")
                        if self.data_sql.db.execute(q).status : insert += 1
            else:
                if bulk :
                    for index, row in data.iloc[::-1].iterrows(): 
                        iter += 1
                        insert += 1
                        query += f"('{row['Date']}',{row['BidOpen']},{row['BidClose']},{row['BidHigh']},{row['BidLow']},{row['AskOpen']},{row['AskClose']},{row['AskHigh']},{row['AskLow']}),"
                    if iter > 0 : query = query[:-1]
                    result = self.data_sql.db.execute(query)
                    if not result.status : insert = 0
                else:
                    for index, row in data.iloc[::-1].iterrows(): 
                        iter += 1
                        q = query + (f"('{row['Date']}',{row['BidOpen']},{row['BidClose']},{row['BidHigh']},{row['BidLow']},{row['AskOpen']},{row['AskClose']},{row['AskHigh']},{row['AskLow']})")
                        if self.data_sql.db.execute(q).status : insert += 1
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = insert
            output.message = f"{instrument} | {timeframe} | {sort(insert, 6)} |"
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
    
    #--------------------------------------------- run
    def store(self, instrument, timeframe, mode, count, repeat, delay, save, bulk, datefrom, dateto):
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
            #--------------Check
            if mode == "up":
                d = self.get_max_min(instrument=instrument, timeframe=timeframe, mode="max", filed="Date")
                if d.status and d.data: datefrom = self.timeframe_nex_date(date=d.data, timeframe=timeframe)
            elif mode == "down":
                d = self.get_max_min(instrument=instrument, timeframe=timeframe, mode="min", filed="Date")
                if d.status and d.data : dateto = self.timeframe_nex_date(date=d.data, timeframe=timeframe)
            #--------------Display
            params = {"account": self.api.name,"instrument": instrument, "timeframe": timeframe, "mode": mode, "count": count, "repeat": repeat, "delay": delay, "save": save, "bulk": bulk, "datefrom": datefrom, "dateto": dateto}
            print(format_dict_block("Store", params))
            #--------------Action
            while(True):
                for r in range(repeat):
                    start = datefrom
                    end = dateto
                    while(True):
                        if (end - start).total_seconds() > 1:
                            history:model_output = self.history(instrument, timeframe, datefrom=start, dateto=end, count=count)
                            if history.status:
                                if save : self.save(instrument=instrument, timeframe=timeframe, data=history.data, bulk=bulk)
                                end = self.timeframe_nex_date(date=history.data["Date"].iloc[0] , timeframe=timeframe)
                                if mode == "once" : break
                            else : break
                        else: break
                if delay == 0: break; 
                time.sleep(delay)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = None
            output.message = f"{instrument} | {timeframe} |"
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
                                self.api.logout()
                                account_cfg = config.get("forex_connect", {}).get(self.api.name, {})
                                forex_api = Forex_Api(
                                    name=self.api.name, 
                                    type=account_cfg.get("type"), 
                                    username=account_cfg.get("username"), 
                                    password=account_cfg.get("password"), 
                                    url=account_cfg.get("url"), 
                                    key=account_cfg.get("key")
                                )
                                self.api = forex_api
                                self.fx = forex_api.fx
                                self.api.login()
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
                        spread = (ask-bid) * point_size 
                        break
            #--------------TP/SL
            if tp_pips or sl_pips:
                if action == "buy":
                    tp = float(f"{ask + (tp_pips * point_size):.{digits}f}")
                    sl = float(f"{bid - (sl_pips * point_size):.{digits}f}")
                elif action == "sell":
                    tp = float(f"{bid - (tp_pips * point_size):.{digits}f}")
                    sl = float(f"{ask + (sl_pips * point_size):.{digits}f}")
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
                        AMOUNT= amount
                    )
                print("------------befor response")
                response = self.fx.send_request(request)
                print("------------after response")
                order_id = getattr(response, "order_id", None) if response else None
                print("------------order_id:", order_id)


            #--------------Result
            if order_id:
                obj = model_live_order_db()
                obj.execute_id = execute_id
                obj.order_id = order_id
                obj.symbol = symbol
                obj.action = action
                obj.amount = amount
                obj.bid = bid
                obj.ask = ask
                obj.tp = tp
                obj.sl = sl
                obj.status = 'open'
                self.data_orm.add(model=model_live_order_db, item=obj)
            else:
                output.status = False
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = order_id
            output.message = f"{execute_id} | {order_id} | {symbol} | {action} | {amount} | {bid} | {ask} | {tp} | {sl}"
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
            #--------------Complete
            time.sleep(3)
            result_complete = self.order_close_complete(order_ids=close_order_ids)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = close_order_ids
            output.message =f"{len(items.data)} | {len(order_ids)} | {len(close_order_ids)} | {result_complete.data}"
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

    #--------------------------------------------- order_close_complete
    def order_close_complete(self, order_ids=None):
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
        complete_count = 0
        
        try:
            #--------------data
            items = self.orader_close_list()
            #--------------Items
            if items.status:
                for item in items.data:
                    order_id = item['open_order_id']
                    gross_pl = item['gross_pl']
                    if order_id in order_ids:
                        obj = self.data_orm.items(model=model_live_order_db, order_id=order_id).data[0]
                        obj.profit = gross_pl
                        obj.status = "close"
                        self.data_orm.update(model=model_live_order_db, item=obj)
                        complete_count += 1
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = complete_count
            output.message =f"{len(items.data)} | {len(order_ids)} | {complete_count}"
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
    