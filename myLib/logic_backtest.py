#--------------------------------------------------------------------------------- Location
# myLib/logic_backtest.py

#--------------------------------------------------------------------------------- Description
# logic_backtest

#--------------------------------------------------------------------------------- Import
import inspect, time, ast
from myLib.logic_global import debug, list_instrument, log_instance, data_instance
from myLib.utils import model_output, sort, get_tbl_name
from myLib.log import Log
from myLib.data_sql import Data_SQL
from myLib.logic_management import Logic_Management
from myModel import *

#--------------------------------------------------------------------------------- Action
class Logic_BackTest:
    #--------------------------------------------- init
    def __init__(self, execute_id, data_sql:Data_SQL=None, management_sql:Data_SQL=None, log:Log=None):
        #--------------------Variable
        self.this_class = self.__class__.__name__
        self.execute_id = execute_id
        self.strategy = None
        self.data = None
        #--------------------Instance
        self.management_sql = management_sql if management_sql else data_instance["management_sql"]
        self.data_sql = data_sql if data_sql else data_instance["data_sql"]
        self.log = log if log else log_instance
        self.logic_management = Logic_Management()

    #--------------------------------------------- execute
    def start(self):
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
            #--------------Detaile
            execute_detaile:model_output = self.logic_management.execute_detaile(id=self.execute_id, mode="back")
            detaile = execute_detaile.data
            strategy_name = detaile.get("strategy_name")
            status = detaile.get("status")
            date_from = detaile.get("date_from")
            date_to = detaile.get("date_to")
            params = ast.literal_eval(detaile.get("params"))
            #--------------Data
            if status !="start":
                symbols = params.get("symbols", "").split(',')
                self.data = self.get_data(symbols=symbols, date_from=date_from, date_to=date_to).data
            #--------------Strategy
            if status !="start" and len(self.data)>0:
                self.strategy = self.logic_management.get_strategy_instance(strategy_name).data
                self.strategy.params = params
            #--------------Start
            if status !="start":
                self.strategy_start()
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 12)} | {sort(this_method, 8)} | {output.time}", output.message)
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
    

    #--------------------------------------------- get_data
    def get_data(self, symbols, date_from, date_to):
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
        output.data = {}

        try:
            #--------------Action
            for symbol in symbols:
                table = get_tbl_name(symbol, "t1")
                cmd = f"SELECT * FROM {table} WHERE date>='{date_from}' and date<='{date_to}' ORDER BY date ASC"
                result:model_output = self.data_sql.db.items(cmd=cmd)
                if result.status == True :
                    output.data[symbol] = result.data
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 12)} | {sort(this_method, 8)} | {output.time}", output.message)
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
    

    #--------------------------------------------- strategy_start
    def strategy_start(self):
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
            #--------------Data
            result:model_output = self.strategy.start()
            #--------------Action
            if result.status == True :
                for item in result.data :
                    bid = self.data["EUR/USD"][0][2]
                    ask = self.data["EUR/USD"][0][3]
                    self.action(item=item, bid=bid, ask=ask)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 12)} | {sort(this_method, 8)} | {output.time}", output.message)
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
    

    #--------------------------------------------- action
    def action(self, item:dict, ask, bid)-> model_output:
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
            run = item.get("run")
            state = item.get("state")
            #--------------order_open
            if run == "order_open":
                #---Data
                buy_sell = item.get("buy_sell")
                symbol = item.get("symbol")
                amount = item.get("amount")
                tp_pips = item.get("tp_pips")
                sl_pips = item.get("sl_pips")
                #---Action
                if tp_pips or sl_pips:
                    point_size = list_instrument[symbol]["point_size"]
                    digits = list_instrument[symbol]["digits"]
                    if buy_sell == "buy":
                        tp = float(f"{ask + tp_pips * point_size:.{digits}f}")
                        sl = float(f"{bid - sl_pips * point_size:.{digits}f}")
                    elif buy_sell == "sell":
                        tp = float(f"{bid - tp_pips * point_size:.{digits}f}")
                        sl = float(f"{ask + sl_pips * point_size:.{digits}f}")
                #---Database
                cmd = f"INSERT INTO back_order (date_from, model, subject, data) VALUES('{dt.now():%Y-%m-%d %H:%M:%S}', '{model}', '{subject}', '{data}')"
                cmd = f"UPDATE back_execute SET status='{state}' WHERE id={self.execute_id}"
                self.data_sql.db.execute(cmd=cmd)


            #--------------close_all_order
            if run == "close_all_order":
                #---Data
                order_ids = []
                cmd = f"SELECT * FROM back_execute WHERE execute_id={self.execute_id} AND status='open'"
                orders = self.data_sql.db.items(cmd=cmd)
                # #---Action
                # if orders.status:
                #     for order in orders.data : order_ids.append(order.order_id)
                #     if len(order_ids)>0 : forex.order_close(order_ids=order_ids)
                # #---Database
                # if order_result.status:
                #     cmd = f"UPDATE live_execute SET status='{state}' WHERE id={execute_id}"
                #     self.data_sql.db.execute(cmd=cmd)
            #--------------Output
            output = None
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 12)} | {sort(this_method, 8)} | {output.time}", output.message)
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