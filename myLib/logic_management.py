#--------------------------------------------------------------------------------- Location
# myLib/logic_management.py

#--------------------------------------------------------------------------------- Description
# logic_management

#--------------------------------------------------------------------------------- Import
import inspect, time, ast
from myLib.model import model_output
from myLib.logic_global import debug, log_instance, data_instance, forex_apis
from myLib.utils import sort
from myLib.log import Log
from myLib.data_orm import Data_Orm
from myLib.data_sql import Data_SQL
from myLib.forex import Forex
from myModel import *
from myStrategy import *

#--------------------------------------------------------------------------------- Class
class Logic_Management:
    #-------------------------- [Init]
    def __init__(
            self,
            data_orm=None, 
            data_sql=None,
            log=None
        ):
        #-------------- Variable
        self.this_class = self.__class__.__name__
        #-------------- Instance
        self.log:Log = log if log else log_instance
        self.data_orm:Data_Orm = data_orm if data_orm else data_instance["management_orm"]
        self.data_sql:Data_SQL = data_sql if data_sql else data_instance["management_sql"]

    #--------------------------------------------- get_strategy_instance
    def get_strategy_instance(self, name)-> model_output:
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
            strategy_class = globals().get(name)
            if strategy_class and callable(strategy_class):
                output.data = strategy_class()
            else:
                output.status = False
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.message=name
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

    #--------------------------------------------- get_strategy_item_instance
    def get_strategy_item_instance(self, strategy_name, params, account_id) -> model_output:
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
            params = ast.literal_eval(params)
            #--------------Action
            forex_api = forex_apis[account_id]
            forex = Forex(forex_api=forex_api)
            strategy = self.get_strategy_instance(strategy_name).data
            strategy.forex = forex
            strategy.params = params
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = strategy
            output.message=f"{strategy_name} | {account_id} | {params}"
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

    #-------------------------- [strategy_item_detail]
    def strategy_item_detail(self, strategy_item_id) -> model_output:
        #-------------- Description
        # IN     : execute_id
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
        detaile = {}

        try:
            #--------------Action
            cmd = f"SELECT strategy.name, strategy_item.params FROM strategy JOIN strategy_item ON strategy.id = strategy_item.strategy_id WHERE strategy_item.id='{strategy_item_id}';"
            result:model_output = self.data_sql.db.items(cmd=cmd)
            #--------------Data
            if result.status and len(result.data) > 0 :
                detaile["strategy_name"] = result.data[0][0]
                detaile["params"] = result.data[0][1]
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = detaile
            output.message=strategy_item_id
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
    
    #-------------------------- [execute_detaile]
    def execute_detaile(self, id) -> model_output:
        #-------------- Description
        # IN     : execute_id
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
        detaile = {}

        try:
            #--------------Action
            cmd = f"SELECT strategy.name, strategy_item.params, live_execute.account_id, live_execute.status FROM strategy JOIN strategy_item ON strategy.id = strategy_item.strategy_id JOIN live_execute ON strategy_item.id = live_execute.strategy_item_id WHERE live_execute.id = '{id}';"
            result:model_output = self.data_sql.db.items(cmd=cmd)
            #--------------Data
            if result.status and len(result.data) > 0 :
                detaile["strategy_name"] = result.data[0][0]
                detaile["params"] = result.data[0][1]
                detaile["account_id"] = result.data[0][2]
                detaile["status"] = result.data[0][3]
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = detaile
            output.message=id
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
    
    #-------------------------- [order_detaile]
    def order_detaile(self, order_id) -> model_output:
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
        detaile = {}

        try:
            #--------------Action
            cmd = f"SELECT strategy.name, strategy_item.params, live_execute.account_id, live_order.id, live_order.date, live_order.symbol, live_order.action, live_order.amount, live_order.bid, live_order.ask, live_order.tp, live_order.sl, live_order.profit, live_order.status FROM strategy JOIN strategy_item ON strategy.id = strategy_item.strategy_id JOIN live_execute ON strategy_item.id = live_execute.strategy_item_id JOIN live_order ON live_order.execute_id = live_execute.id WHERE live_order.order_id = '{order_id}';"
            result:model_output = self.data_sql.db.items(cmd=cmd)
            #--------------Data
            if result.status and len(result.data) > 0 :
                detaile["strategy_name"] = result.data[0][0]
                detaile["params"] = result.data[0][1]
                detaile["account_id"] = result.data[0][2]
                detaile["live_order_id"] = result.data[0][3]
                detaile["date"] = result.data[0][4]
                detaile["symbol"] = result.data[0][5]
                detaile["action"] = result.data[0][6]
                detaile["amount"] = result.data[0][7]
                detaile["bid"] = result.data[0][8]
                detaile["ask"] = result.data[0][9]
                detaile["tp"] = result.data[0][10]
                detaile["sl"] = result.data[0][11]
                detaile["profit"] = result.data[0][12]
                detaile["status"] = result.data[0][13]
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = detaile
            output.message=order_id
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
        
    #-------------------------- [order_close]
    def order_close(self, order_id) -> model_output:
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
            cmd = f"UPDATE live_order SET status='close' WHERE order_id = '{order_id}';"
            result:model_output = self.data_sql.db.execute(cmd=cmd)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = order_id
            output.message=f"{order_id}"
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