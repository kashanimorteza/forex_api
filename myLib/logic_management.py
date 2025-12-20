#--------------------------------------------------------------------------------- Location
# myLib/logic_management.py

#--------------------------------------------------------------------------------- Description
# logic_management

#--------------------------------------------------------------------------------- Import
import inspect, time, ast
from myLib.logic_global import debug, log_instance, data_instance, forex_apis
from myLib.utils import model_output, sort
from myLib.log import Log
from myLib.data_orm import Data_Orm
from myLib.data_sql import Data_SQL
from myLib.logic_forex import Logic_Forex
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
            #--------------Data
            table = "live_execute" if mode == "live" else "back_execute"
            #--------------Action
            cmd_live = f"SELECT strategy.name, strategy_item.params, {table}.account_id, {table}.status FROM strategy JOIN strategy_item ON strategy.id = strategy_item.strategy_id JOIN {table} ON strategy_item.id = {table}.strategy_item_id WHERE {table}.id = '{id}';"
            cmd_back = f"SELECT strategy.name, strategy_item.params, {table}.account_id, {table}.status, {table}.date_from, {table}.date_to FROM strategy JOIN strategy_item ON strategy.id = strategy_item.strategy_id JOIN {table} ON strategy_item.id = {table}.strategy_item_id WHERE {table}.id = '{id}';"
            cmd = cmd_live if mode == "live" else cmd_back
            result:model_output = self.data_sql.db.items(cmd=cmd)
            #--------------Data
            if result.status and len(result.data) > 0 :
                detaile["strategy_name"] = result.data[0][0]
                detaile["params"] = result.data[0][1]
                detaile["account_id"] = result.data[0][2]
                detaile["status"] = result.data[0][3]
                if mode == "back":
                    detaile["date_from"] = result.data[0][4]
                    detaile["date_to"] = result.data[0][5]
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
    
    #-------------------------- [order_detaile]
    def order_detaile(self, order_id, mode="live") -> model_output:
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
            #--------------Data
            table = "live_execute" if mode == "live" else "back_execute"
            #--------------Action
            cmd_live = f"SELECT strategy.name, strategy_item.params, {table}.id, {table}.account_id, live_order.id, live_order.trade_id, live_order.date, live_order.symbol, live_order.action, live_order.amount, live_order.bid, live_order.ask, live_order.tp, live_order.sl, live_order.profit, live_order.status, {table}.status FROM strategy JOIN strategy_item ON strategy.id = strategy_item.strategy_id JOIN {table} ON strategy_item.id = {table}.strategy_item_id JOIN live_order ON live_order.execute_id = {table}.id WHERE live_order.order_id='{order_id}'"
            cmd_back = f"SELECT strategy.name, strategy_item.params, {table}.id, {table}.account_id, back_order.id, back_order.trade_id, back_order.date_open, back_order.symbol, back_order.action, back_order.amount, back_order.bid, back_order.ask, back_order.tp, back_order.sl, back_order.profit, back_order.status, {table}.status, back_order.date_open, back_order.date_close FROM strategy JOIN strategy_item ON strategy.id = strategy_item.strategy_id JOIN {table} ON strategy_item.id = {table}.strategy_item_id JOIN back_order ON back_order.execute_id = {table}.id WHERE back_order.id='{order_id}'"
            cmd = cmd_live if mode == "live" else cmd_back
            result:model_output = self.data_sql.db.items(cmd=cmd)
            #--------------Detaile
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
                if mode == "back":
                    detaile["date_open"] = result.data[0][17]
                    detaile["date_close"] = result.data[0][18]
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = detaile
            output.message=order_id
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
        #-------------- Output
        result = model_output()

        try:
            #--------------Data
            if execute_id:
                execute_detaile = self.execute_detaile(id=execute_id).data
                strategy_name = execute_detaile["strategy_name"]
                params = execute_detaile["params"]
                params = ast.literal_eval(params)
                account_id = execute_detaile["account_id"]
            else:
                execute_id = order_detaile["execute_id"]
                strategy_name = order_detaile["strategy_name"]
                params = order_detaile["params"]
                account_id = order_detaile["account_id"]
            #--------------strategy
            strategy = self.get_strategy_instance(strategy_name).data
            strategy.params = params
            #--------------Action
            if action == "start" : result = strategy.start()
            if action == "stop" : result = strategy.stop()
            if action == "order_close" : result = strategy.order_close(order_detaile=order_detaile)
            if action == "price_change" : result = strategy.price_change(order_detaile=order_detaile)
            #--------------Action
            if result.status:
                forex:Logic_Forex = forex_apis[account_id]
                for item in result.data:
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
                        order_result:model_output = forex.order_open(
                            action=buy_sell, 
                            symbol=symbol,
                            amount=amount,
                            tp_pips=tp_pips,
                            sl_pips=sl_pips,
                            execute_id=execute_id
                        )
                        #---Database
                        if order_result.status:
                            cmd = f"UPDATE live_execute SET status='{state}' WHERE id={execute_id}"
                            self.data_sql.db.execute(cmd=cmd)
                    #--------------close_all_order
                    if run == "close_all_order":
                        #---Data
                        order_ids = []
                        cmd = f"SELECT * FROM live_execute WHERE execute_id={execute_id} AND status='open'"
                        orders = self.data_sql.db.items(cmd=cmd)
                        #---Action
                        if orders.status:
                            for order in orders.data : order_ids.append(order.order_id)
                            if len(order_ids)>0 : forex.order_close(order_ids=order_ids)
                        #---Database
                        if order_result.status:
                            cmd = f"UPDATE live_execute SET status='{state}' WHERE id={execute_id}"
                            self.data_sql.db.execute(cmd=cmd)
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
    
    #-------------------------- [order_close]
    def back_test(self, execute_id, trade_id, profit) -> model_output:
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