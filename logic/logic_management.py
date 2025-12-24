#--------------------------------------------------------------------------------- Location
# logic/logic_management.py

#--------------------------------------------------------------------------------- Description
# logic_management

#--------------------------------------------------------------------------------- Import
import inspect, time, ast

from sqlalchemy import table
from logic.logic_global import debug, log_instance, data_instance, forex_apis, Strategy_Run, Strategy_Action
from logic.logic_util import model_output, sort
from logic.logic_log import Logic_Log
from logic.data_orm import Data_Orm
from logic.data_sql import Data_SQL
from model import *
from strategy import *

#--------------------------------------------------------------------------------- Class
class Logic_Management:
    #-------------------------- [Init]
    def __init__(self,
        data_orm:Data_Orm=None,
        data_sql:Data_SQL=None,
        log:Logic_Log=None
        ):
        #-------------- Variable
        self.this_class = self.__class__.__name__
        #-------------- Instance
        self.data_orm = data_orm if data_orm else data_instance["management_orm"]
        self.data_sql = data_sql if data_sql else data_instance["management_sql"]
        self.log = log if log else log_instance

    #--------------------------------------------- get_strategy_instance
    def get_strategy_instance(self, name, execute_detaile)-> model_output:
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
                output.data = strategy_class(params=execute_detaile)
            else:
                output.status = False
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.message=name
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
    def execute_detaile(self, id, mode="live") -> model_output:
        #-------------- Variable
        output = {}
        #--------------Data
        table = "live_execute" if mode == "live" else "back_execute"
        #--------------Action
        cmd = f"SELECT strategy.name, strategy_item.symbols, strategy_item.actions, strategy_item.amount, strategy_item.tp_pips, strategy_item.sl_pips, strategy_item.limit_trade, strategy_item.limit_profit, strategy_item.limit_loss, strategy_item.params, {table}.date_from, {table}.date_to, {table}.account_id, {table}.step, {table}.status FROM strategy JOIN strategy_item ON strategy.id = strategy_item.strategy_id JOIN {table} ON strategy_item.id = {table}.strategy_item_id WHERE {table}.id = {id}"
        result:model_output = self.data_sql.db.items(cmd=cmd)
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
    def order_detaile(self, order_id, mode="live") -> model_output:
        #-------------- Variable
        output = {}
        #--------------Data
        if mode == "live":
            table1 = "live_execute" 
            table2 = "live_order"
        else:
            table1 = "back_execute" 
            table2 = "back_order"
        #--------------Action
        cmd = f"SELECT strategy.name, strategy_item.id,{table1}.status, {table1}.id, {table1}.account_id, {table2}.execute_id, {table2}.step, {table2}.father_id, {table2}.date_open, {table2}.price_open, {table2}.date_close, {table2}.price_close, {table2}.profit, {table2}.status,{table2}.symbol, {table2}.action, {table2}.amount, {table2}.tp, {table2}.sl, {table2}.trade_id, {table2}.enable FROM strategy JOIN strategy_item ON strategy.id = strategy_item.strategy_id JOIN {table1} ON strategy_item.id = {table1}.strategy_item_id JOIN {table2} ON {table1}.id = {table2}.execute_id WHERE {table2}.order_id='{order_id}'"
        result:model_output = self.data_sql.db.items(cmd=cmd)
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
