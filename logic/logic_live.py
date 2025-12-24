#--------------------------------------------------------------------------------- Location
# logic/logic_live.py

#--------------------------------------------------------------------------------- Description
# logic_live

#--------------------------------------------------------------------------------- Import
import inspect, time
from datetime import timedelta
from logic.logic_global import debug, log_instance, data_instance, Strategy_Run, Strategy_Action, forex_apis
from logic.logic_util import model_output, sort, get_tbl_name, format_dict_block, get_strategy_instance
from logic.logic_log import Logic_Log
from logic.data_sql import Data_SQL
from logic.fxcm_api import Fxcm_API
from model import *

#--------------------------------------------------------------------------------- Action
class Logic_Live:
    #--------------------------------------------- init
    def __init__(self, account_info:dict=None, data_sql:Data_SQL=None, management_sql:Data_SQL=None, log:Logic_Log=None):
        #--------------------Variable
        self.this_class = self.__class__.__name__
        self.account_info = account_info
        self.api_name = None
        #--------------------Instance
        self.management_sql = management_sql if management_sql else data_instance["management_sql"]
        self.data_sql = data_sql if data_sql else data_instance["data_sql"]
        self.log = log if log else log_instance
        #--------------------Api
        if account_info:
            if self.account_info.get("broker").lower() == "fxcm":
                self.api = Fxcm_API(account_info=self.account_info)
                self.api_name = "Fxcm_API"
            else:
                self.api = Fxcm_API(account_info=self.account_info)
                self.api_name = "Fxcm_API"

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
        start_time = time.time()
        #-------------- Output
        output = model_output()
        output.class_name = self.this_class
        output.method_name = this_method

        try:
            #--------------Action
            result:model_output = self.api.login()
            #--------------Output
            output = result
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 12)} | {output.time}", output.message)
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
            result:model_output = self.api.logout()
            #--------------Output
            output = result
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 12)} | {output.time}", output.message)
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

    #--------------------------------------------- info
    def info(self):
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

        try:
            #--------------Action
            result:model_output = self.api.info()
            #--------------Output
            output = result
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 12)} | {output.time}", output.message)
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
            #--------------Action
            result:model_output = self.api.instruments()
            #--------------Output
            output = result
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 12)} | {output.time}", output.message)
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
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 12)} | {output.time}", output.message)
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
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 12)} | {output.time}", output.message)
            #--------------Log
            if log : self.log.log(log_model, output)
        except Exception as e:  
            #--------------Error
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
            raise
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
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 12)} | {output.time}", output.message)
            #--------------Log
            if log : self.log.log(log_model, output)
        except Exception as e:  
            #--------------Error
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
            raise
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

        try:
            #--------------Action
            result:model_output = self.api.history(instrument, timeframe, datefrom=datefrom, dateto=dateto, count=count)
            #--------------Output
            output = result
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 12)} | {output.time}", output.message)
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

    #--------------------------------------------- get_table
    def get_table(self, table):
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
        
        try:
            #--------------Action
            result:model_output = self.api.get_table(table = table)
            #--------------Output
            output = result
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 12)} | {output.time}", output.message)
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
    def order_open(self, symbol, action, amount, tp_pips, sl_pips, execute_id, step, father_id):
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
            result:model_output = self.api.order_open(symbol, action, amount, tp_pips, sl_pips, execute_id)
            #--------------Database
            if result.status:
                order_id, bid, ask, tp, sl, price_open, date_open = result.data
                cmd = f"INSERT INTO live_order (execute_id, order_id, step, father_id, date_open, price_open, symbol, action, amount, tp, sl, status, trade_id, profit, enable) VALUES ({execute_id}, '{order_id}', '{step}', '{father_id}', '{date_open}', '{price_open}', '{symbol}', '{action}', {amount}, {tp}, {sl}, 'open', '', 0.0, True)"
                self.management_sql.db.execute(cmd=cmd)
            #--------------Output
            output = result
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 12)} | {output.time}", output.message)
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

    #-------------------------- [order_closed]
    def order_closed(self, order_id, trade_id, profit, date_close, price_close) -> model_output:
        #-------------- Description
        # IN     : order_id | profit
        # OUT    : model_output
        # Action : update order on database:status,profit | get strategy and run action order_close
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
            #--------------Database
            cmd = f"UPDATE live_order SET trade_id='{trade_id}', status='close', profit={profit}, date_close='{date_close}', price_close={price_close} WHERE order_id='{order_id}'"
            self.management_sql.db.execute(cmd=cmd)
            #--------------Strategy
            order_detaile = self.order_detaile(order_id=order_id)
            if order_detaile["execute_status"] != "stop" : self.strategy_action(action=Strategy_Action.ORDER_CLOSE, order_detaile=order_detaile)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = order_detaile
            output.message = f"{order_id} | {profit}"
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
    
    #--------------------------------------------- order_close
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

        try:
            #--------------Action
            result:model_output = self.api.order_close(order_ids=order_ids)
            #--------------Output
            output=result
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 12)} | {output.time}", output.message)
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

    #--------------------------------------------- order_close_update
    def order_close_update(self, order_ids=None):
        #-------------- Description
        # IN     : list of order_id
        # OUT    : model_output
        # Action : Get all close trades and update live_order table with profit and status='close'
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
        count = 0
        
        try:
            #--------------data
            result:model_output = self.api.get_table("CLOSED_TRADES")
            #--------------Items
            if result.status:
                for item in result.data:
                    order_id = item['open_order_id']
                    gross_pl = item['gross_pl']
                    if order_id in order_ids:
                        cmd = f"UPDATE live_order SET profit={gross_pl}, status='close' WHERE order_id='{order_id}'"
                        self.management_sql.db.execute(cmd=cmd)
                        count += 1
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = count
            output.message =f"{len(result.data)} | {len(order_ids)} | {count}"
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 12)} | {output.time}", output.message)
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
    
    #-------------------------- [order_count]
    def order_count(self, execute_id) -> model_output:
        #-------------- Description
        # IN     : execute_id
        # OUT    : model_output
        # Action : Get all order, seperate to All/Close/Open, Detaile for each order
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
            cmd = f"SELECT max(count) FROM live_order WHERE execute_id={execute_id}"
            max_count = self.management_sql.db.items(cmd=cmd).data[0][0]
            if max_count is None : max_count = 0
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = max_count
            output.message=max_count
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 12)} | {output.time}", output.message)
            #--------------Log
            if log : self.log.log(log_model, output)
        except Exception as e:  
            #--------------Error
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Return
        return max_count
    
    #-------------------------- [order_clear]
    def order_clear(self, execute_id) -> model_output:
        #-------------- Description
        # IN     : execute_id
        # OUT    : model_output
        # Action : Get all order, seperate to All/Close/Open, Detaile for each order
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
            #--------------Acion
            cmd = f"DELETE FROM live_order WHERE execute_id={execute_id}"
            self.management_sql.db.execute(cmd=cmd)
            cmd = f"DELETE FROM live_execute_detaile WHERE execute_id={execute_id}"
            self.management_sql.db.execute(cmd=cmd)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = None
            output.message=None
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 12)} | {output.time}", output.message)
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
    
    #-------------------------- [strategy_action]
    def strategy_action(
                    self, 
                    execute_id=None, 
                    action:Strategy_Action=None,
                    order_detaile=None
                    ) -> model_output:
        #-------------- Description
        # IN     : 
        # OUT    : model_output
        # Action : run strategy action
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
            #--------------Data
            if execute_id:
                execute_detaile = self.execute_detaile(id=execute_id)
                strategy_name = execute_detaile["strategy_name"]
                account_id = execute_detaile["account_id"]
            else:
                execute_id = order_detaile["execute_id"]
                execute_detaile = self.execute_detaile(id=execute_id)
                strategy_name = order_detaile["strategy_name"]
                account_id = order_detaile["account_id"]
                step = order_detaile["step"]
                father_id = order_detaile["father_id"]
            #--------------strategy
            strategy = get_strategy_instance(strategy_name, execute_detaile).data
            #--------------Action
            if action == Strategy_Action.START : 
                result:model_output = strategy.start()
                cmd = f"SELECT MAX(step) FROM live_order WHERE execute_id='{execute_id}'"
                step = self.management_sql.db.items(cmd=cmd).data[0][0]
                step = step + 1 if step else 1
                father_id=0
            elif action == Strategy_Action.STOP : 
                result:model_output = strategy.stop()
            elif action == Strategy_Action.ORDER_CLOSE : 
                result:model_output = strategy.order_close(order_detaile)
            elif action == Strategy_Action.PRICE_CHANGE : 
                result:model_output = strategy.price_change(order_detaile)
            #--------------Action
            if result.status:
                forex:Logic_Live = forex_apis[account_id]
                for item in result.data:
                    run = item.get("run")
                    state = item.get("state")
                    #--------------order_open
                    if run == Strategy_Run.ORDER_OPEN :
                        #---Action
                        order_result:model_output = forex.order_open(
                            action=item.get("action"), 
                            symbol=item.get("symbol"),
                            amount=item.get("amount"),
                            tp_pips=item.get("tp_pips"),
                            sl_pips=item.get("sl_pips"),
                            execute_id=execute_id,
                            step=step,
                            father_id=father_id
                        )
                        #---Database
                        if order_result.status:
                            cmd = f"UPDATE live_execute SET status='{state}' WHERE id={execute_id}"
                            self.management_sql.db.execute(cmd=cmd)
                    #--------------close_all_order
                    if run == Strategy_Run.ORDER_CLOSE_ALL:
                        #---Data
                        order_ids = []
                        cmd = f"SELECT order_id FROM live_order WHERE execute_id={execute_id} AND status='open'"
                        orders = self.management_sql.db.items(cmd=cmd)
                        #---Action
                        if orders.status:
                            for order in orders.data : order_ids.append(order[0])
                            if len(order_ids)>0 :
                                #-Database
                                cmd = f"UPDATE live_execute SET status='{state}' WHERE id={execute_id}"
                                self.management_sql.db.execute(cmd=cmd)
                                #-forex 
                                order_result:model_output = forex.order_close(order_ids=order_ids)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = None
            output.message = None
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 12)} | {output.time}", output.message)
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
    
    #-------------------------- [execute_detaile]
    def execute_detaile(self, id) -> model_output:
        #-------------- Variable
        output = {}
        #--------------Data
        table = "live_execute"
        #--------------Action
        cmd = f"SELECT strategy.name, strategy_item.symbols, strategy_item.actions, strategy_item.amount, strategy_item.tp_pips, strategy_item.sl_pips, strategy_item.limit_trade, strategy_item.limit_profit, strategy_item.limit_loss, strategy_item.params, {table}.date_from, {table}.date_to, {table}.account_id, {table}.step, {table}.status FROM strategy JOIN strategy_item ON strategy.id = strategy_item.strategy_id JOIN {table} ON strategy_item.id = {table}.strategy_item_id WHERE {table}.id = {id}"
        result:model_output = self.management_sql.db.items(cmd=cmd)
        #--------------Data
        if result.status and len(result.data) > 0 :
            output["strategy_name"] = result.data[0][0]
            output["symbols"] = result.data[0][1]
            output["actions"] = result.data[0][2]
            output["amount"] = result.data[0][3]
            output["tp_pips"] = result.data[0][4]
            output["sl_pips"] = result.data[0][5]
            output["limit_trade"] = result.data[0][6]
            output["limit_profit"] = result.data[0][7]
            output["limit_loss"] = result.data[0][8]
            output["params"] = ast.literal_eval(result.data[0][9]) if result.data[0][9] else {}
            output["date_from"] = result.data[0][10]
            output["date_to"] = result.data[0][11]
            output["account_id"] = result.data[0][12]
            output["step"] = result.data[0][13]
            output["status"] = result.data[0][14]
        #--------------Return
        return output
    
    #-------------------------- [order_detaile]
    def order_detaile(self, order_id) -> model_output:
        #-------------- Variable
        output = {}
        #--------------Data
        table1 = "live_execute" 
        table2 = "live_order"
        #--------------Action
        cmd = f"SELECT strategy.name, strategy_item.id,{table1}.status, {table1}.id, {table1}.account_id, {table2}.execute_id, {table2}.step, {table2}.father_id, {table2}.date_open, {table2}.price_open, {table2}.date_close, {table2}.price_close, {table2}.profit, {table2}.status,{table2}.symbol, {table2}.action, {table2}.amount, {table2}.tp, {table2}.sl, {table2}.trade_id, {table2}.enable FROM strategy JOIN strategy_item ON strategy.id = strategy_item.strategy_id JOIN {table1} ON strategy_item.id = {table1}.strategy_item_id JOIN {table2} ON {table1}.id = {table2}.execute_id WHERE {table2}.order_id='{order_id}'"
        result:model_output = self.management_sql.db.items(cmd=cmd)
        #--------------Data
        if result.status and len(result.data) > 0 :
            output["strategy_name"] = result.data[0][0]
            output["strategy_item_id"] = result.data[0][1]
            output["execute_status"] = result.data[0][2]
            output["id"] = result.data[0][3]
            output["account_id"] = result.data[0][4]
            output["execute_id"] = result.data[0][5]
            output["step"] = result.data[0][6]
            output["father_id"] = result.data[0][7]
            output["date_open"] = result.data[0][8]
            output["price_open"] = result.data[0][9]
            output["date_close"] = result.data[0][10]
            output["price_close"] = result.data[0][11]
            output["profit"] = result.data[0][12]
            output["status"] = result.data[0][13]
            output["symbol"] = result.data[0][14]
            output["action"] = result.data[0][15]
            output["amount"] = result.data[0][16]
            output["tp"] = result.data[0][17]
            output["sl"] = result.data[0][18]
            output["trade_id"] = result.data[0][19]
            output["enable"] = result.data[0][20]
        #--------------Return
        return output

    #-------------------------- [execute_order_detaile]
    def execute_order_detaile(self, id, mode="live") -> model_output:
        #-------------- Description
        # IN     : execute_id
        # OUT    : model_output
        # Action : Get all order, seperate to All/Close/Open, Detaile for each order
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
        #-------------- Detaile
        detaile = {}
        all_count = close_count = open_count = all_amount = close_amount = open_amount = all_profit = close_profit = open_profit = all_buy = close_buy = open_buy = all_sell = close_sell = open_sell = 0

        try:
            #--------------Data
            data:model_output = self.data_orm.items(model=model_live_order_db, execute_id=id)
            #--------------Action
            if data.status:
                orders:list[model_live_order_db] = data.data
                for order in orders:
                    #---All
                    all_count += 1
                    all_amount += order.amount
                    all_profit += order.profit
                    all_buy += 1 if order.action == 'buy' else 0; all_sell += 1 if order.action == 'sell' else 0
                    #---Close
                    if order.status == 'close':
                        close_count += 1
                        close_amount += order.amount
                        close_profit += order.profit
                        close_buy += 1 if order.action == 'buy' else 0; close_sell += 1 if order.action == 'sell' else 0
                    #---Open
                    if order.status == 'open':
                        open_count += 1
                        open_amount += order.amount
                        open_profit += order.profit
                        open_buy += 1 if order.action == 'buy' else 0; open_sell += 1 if order.action == 'sell' else 0
                detaile["all"] = {"count":all_count, "amount":all_amount/100000, "profit":round(all_profit, 2), "buy":all_buy, "sell":all_sell}
                detaile["close"] = {"count":close_count, "amount":close_amount/100000, "profit":round(close_profit, 2), "buy":close_buy, "sell":close_sell}
                detaile["open"] = {"count":open_count, "amount":open_amount/100000, "profit":round(open_profit, 2), "buy":open_buy, "sell":open_sell}
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = detaile
            output.message=id
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 12)} | {output.time}", output.message)
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
