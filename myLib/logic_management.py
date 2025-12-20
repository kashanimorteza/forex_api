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
from myModel import *
from myStrategy import *

#--------------------------------------------------------------------------------- Class
class Logic_Management:
    #-------------------------- [Init]
    def __init__(self, data_orm:Data_Orm=None, data_sql:Data_SQL=None, log:Log=None):
        #-------------- Variable
        self.this_class = self.__class__.__name__
        #-------------- Instance
        self.data_orm = data_orm if data_orm else data_instance["management_orm"]
        self.data_sql = data_sql if data_sql else data_instance["management_sql"]
        self.log = log if log else log_instance

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

    #--------------------------------------------- get_strategy_item_instance
    def get_strategy_item_instance(self, strategy_name, params, account_id, execute_id) -> model_output:
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
            strategy = self.get_strategy_instance(strategy_name).data
            strategy.forex = forex_apis[account_id]
            strategy.params = params
            strategy.execute_id = execute_id
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = strategy
            output.message=f"{strategy_name} | {account_id} | {params}"
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 12)} | {sort(this_method, 8)} | {output.time}", output.message)
            #--------------Log
            if log : self.log.log(log_model, output)
        except Exception as e:  
            #--------------Error
            output.status = False
            output.data = None
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
            cmd = f"SELECT strategy.name, strategy_item.params, live_execute.id, live_execute.account_id, live_order.id, live_order.trade_id, live_order.date, live_order.symbol, live_order.action, live_order.amount, live_order.bid, live_order.ask, live_order.tp, live_order.sl, live_order.profit, live_order.status, live_execute.status FROM strategy JOIN strategy_item ON strategy.id = strategy_item.strategy_id JOIN live_execute ON strategy_item.id = live_execute.strategy_item_id JOIN live_order ON live_order.execute_id = live_execute.id WHERE live_order.order_id='{order_id}'"
            result:model_output = self.data_sql.db.items(cmd=cmd)
            #--------------Data
            if result.status and len(result.data) > 0 :
                detaile["strategy_name"] = result.data[0][0]
                detaile["params"] = result.data[0][1]
                detaile["execute_id"] = result.data[0][2]
                detaile["account_id"] = result.data[0][3]
                detaile["order_id"] = result.data[0][4]
                detaile["trade_id"] = result.data[0][5]
                detaile["date"] = result.data[0][6]
                detaile["symbol"] = result.data[0][7]
                detaile["action"] = result.data[0][8]
                detaile["amount"] = result.data[0][9]
                detaile["bid"] = result.data[0][10]
                detaile["ask"] = result.data[0][11]
                detaile["tp"] = result.data[0][12]
                detaile["sl"] = result.data[0][13]
                detaile["profit"] = result.data[0][14]
                detaile["status"] = result.data[0][15]
                detaile["execute_status"] = result.data[0][16]
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = detaile
            output.message=order_id
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
        
    #-------------------------- [strategy_action]
    def strategy_action(self, execute_id=None, action="start", order_detaile=None) -> model_output:
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
                execute_detaile = self.execute_detaile(id=execute_id).data
                strategy_name = execute_detaile["strategy_name"]
                params = execute_detaile["params"]
                account_id = execute_detaile["account_id"]
            else:
                execute_id = order_detaile["execute_id"]
                strategy_name = order_detaile["strategy_name"]
                params = order_detaile["params"]
                account_id = order_detaile["account_id"]
            strategy = self.get_strategy_item_instance(strategy_name=strategy_name, params=params, account_id=account_id, execute_id=execute_id).data
            #--------------Action
            if action == "start" : strategy.start()
            if action == "stop" : strategy.stop()
            if action == "order_close" : strategy.order_close(order_detaile=order_detaile)
            if action == "price_change" : strategy.price_change(order_detaile=order_detaile)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = None
            output.message = None
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
    
    #-------------------------- [execute_order_detaile]
    def execute_order_detaile(self, id) -> model_output:
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
    
    #-------------------------- [order_close]
    def order_close(self, order_id, trade_id, profit) -> model_output:
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
            cmd = f"UPDATE live_order SET trade_id='{trade_id}', status='close', profit={profit} WHERE order_id='{order_id}'"
            self.data_sql.db.execute(cmd=cmd)
            #--------------Strategy
            order_detaile = self.order_detaile(order_id=order_id)
            if order_detaile.status:
                order_detaile = order_detaile.data
                if order_detaile["execute_status"] != "stop" : 
                    result:model_output = self.strategy_action(action="order_close", order_detaile=order_detaile)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = order_detaile
            output.message = f"{order_id} | {profit}"
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