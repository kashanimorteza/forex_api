#--------------------------------------------------------------------------------- Location
# logic/logic_live.py

#--------------------------------------------------------------------------------- Description
# logic_live

#--------------------------------------------------------------------------------- Import
import inspect, time
from datetime import timedelta
from logic.logic_global import debug, log_instance, data_instance
from logic.logic_util import model_output, sort, get_tbl_name, format_dict_block
from logic.logic_log import Logic_Log
from logic.data_sql import Data_SQL
from logic.fxcm_api import Fxcm_API
from model import *

#--------------------------------------------------------------------------------- Action
class Logic_Live:
    #--------------------------------------------- init
    def __init__(self, account_info:dict, data_sql:Data_SQL=None, management_sql:Data_SQL=None, log:Logic_Log=None):
        #--------------------Variable
        self.this_class = self.__class__.__name__
        self.account_info = account_info
        self.api_name = None
        #--------------------Instance
        self.management_sql = management_sql if management_sql else data_instance["management_sql"]
        self.data_sql = data_sql if data_sql else data_instance["data_sql"]
        self.log = log if log else log_instance
        #--------------------Api
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
                cmd = f"INSERT INTO live_order (execute_id, order_id, step, father_id, date_open, price_open, symbol, action, amount, bid, ask, tp, sl, status, trade_id, profit, enable) VALUES ({execute_id}, '{order_id}', '{step}', '{father_id}', '{date_open}', '{price_open}', '{symbol}', '{action}', {amount}, {bid}, {ask}, {tp}, {sl}, 'open', '', 0.0, True)"
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