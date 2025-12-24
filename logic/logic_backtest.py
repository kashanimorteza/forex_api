#--------------------------------------------------------------------------------- Location
# logic/logic_backtest.py

#--------------------------------------------------------------------------------- Description
# logic_backtest

#--------------------------------------------------------------------------------- Import
import inspect, time, ast
from logic.logic_global import debug, list_instrument, log_instance, data_instance, Strategy_Run, database_management, database_data
from logic.logic_util import model_output, sort, get_tbl_name, get_strategy_instance
from logic.logic_log import Logic_Log
from logic.data_sql import Data_SQL
from logic.data_orm import Data_Orm
from model.model_back_order import model_back_order_db

#--------------------------------------------------------------------------------- Action
class Logic_BackTest:
    #--------------------------------------------- init
    def __init__(self, 
            execute_id=None,
            management_sql:Data_SQL=None, 
            management_orm:Data_Orm=None, 
            data_sql:Data_SQL=None, 
            log:Logic_Log=None
        ):
        #--------------------Variable
        self.this_class = self.__class__.__name__
        self.execute_id = execute_id
        self.step = 1
        #--------------------Instance
        #---management_orm
        self.management_orm = management_orm if management_orm else Data_Orm(database=database_management)
        #---management_sql
        if management_sql:
            self.management_sql = management_sql
        else:
            self.management_sql = Data_SQL(database=database_management)
            self.management_sql.db.open()
        #---data_sql
        if data_sql:
            self.data_sql = data_sql
        else:
            self.data_sql = Data_SQL(database=database_data)
            self.data_sql.db.open()
        #---log
        self.log = log if log else log_instance

    #--------------------------------------------- run
    def run(self):
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
        data_params = []

        try:
            #--------------Detaile
            execute_detaile:model_output = self.logic_management.execute_detaile(id=self.execute_id, mode="back")
            self.date_from = execute_detaile.get("date_from")
            self.date_to = execute_detaile.get("date_to")
            strategy_name = execute_detaile.get("strategy_name")
            symbols = execute_detaile.get("symbols", "").split(',')
            count = execute_detaile.get("step")
            #--------------Count
            cmd = f"SELECT MAX(step) FROM back_order WHERE execute_id='{self.execute_id}'"
            count_history = self.management_sql.db.items(cmd=cmd).data[0][0]
            if count_history:
                self.step = count+1
            else:
                self.step = 1
            #--------------Strategy
            self.strategy = get_strategy_instance(strategy_name, execute_detaile).data
            #--------------Data
            for symbol in symbols : data_params.append({"symbol": symbol, "date_from":self.date_from, "date_to": self.date_to})
            self.data = self.get_data(params=data_params).data
            #--------------Action
            for i in range(count):
                #--------------Variable
                self.account_profit = 0
                self.account_loss = 0
                self.list_order_open = []
                self.list_order_close = []
                #--------------Start
                result_start:model_output = self.start()
                #--------------Next
                result_next:model_output = self.next()
                #--------------Increase count
                self.step += 1
                #--------------Database
                cmd = f"UPDATE back_execute SET status='stop' WHERE id={self.execute_id}"
                result_database:model_output = self.management_sql.db.execute(cmd=cmd)
                #--------------Output
                output.time = sort(f"{(time.time() - start_time):.3f}", 3)
                output.message = f"{result_start.status} | {result_next.status}"
                #--------------Verbose
                if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 12)} | {output.time}", output.message)
                #--------------Log
                if log : self.log.log(log_model, output)
            #--------------Database
            self.management_sql.db.close()
            self.data_sql.db.close()
        except Exception as e:  
            #--------------Error
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Return
        return output

    #--------------------------------------------- start
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
        #-------------- Variable
        keep = False

        try:
            #--------------Data
            result_strategy:model_output = self.strategy.start()
            #--------------Items
            for item in result_strategy.data :
                if len(self.data[item.get("symbol")])>0:
                    item["father_id"] = 0
                    item["date"] = self.data[item.get("symbol")][0][1]
                    item["ask"] = self.data[item.get("symbol")][0][2]
                    item["bid"] = self.data[item.get("symbol")][0][3]
                    self.data[item.get("symbol")].pop(0)
                    state = item.get("state")
                    keep = True
                else:
                    keep = False
            #--------------Action
            if keep :
                result_action:model_output = self.action(items=result_strategy.data)
            #--------------Database
            if keep :
                cmd = f"UPDATE back_execute SET status='{state}' WHERE id={self.execute_id}"
                result_database:model_output = self.management_sql.db.execute(cmd=cmd)
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

    #--------------------------------------------- next
    def next(self):
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
        result = model_output()
        output.class_name = self.this_class
        output.method_name = this_method
        #-------------- Output
        order_open_accept = True

        try:
            #--------------Action
            for symbol in self.data:
                for row in self.data[symbol]:
                    date = row[1]
                    ask = row[2]
                    bid = row[3]
                    #---Check orders
                    if len(self.list_order_open) > 0:
                        #---Check TP/SL
                        check_tp_sl = self.check_tp_sl(symbol=symbol, ask=ask, bid=bid, date=date)
                        for item in check_tp_sl :
                            item = self.order_close(item = item).data
                            if order_open_accept:
                                order_id = item.get("id")
                                result_strategy:model_output = self.strategy.order_close(order_detaile=item)
                                for item in result_strategy.data :
                                    item["father_id"] = order_id
                                    item["date"] = date
                                    item["ask"] = ask
                                    item["bid"] = bid
                                    self.action(items=result_strategy.data)
                        #---Check limit
                        check_limit_status, check_limit_param  = self.check_limit(ask, bid, date)
                        if not check_limit_status:
                            if check_limit_param == 'trade':
                                order_open_accept = False
                            if check_limit_param == 'profit':
                                order_open_accept = False
                            if check_limit_param == 'loss':
                                result_strategy:model_output = self.strategy.stop()
                                for item in result_strategy.data :
                                    item["father_id"] = -1
                                    item["date"] = date
                                    item["ask"] = ask
                                    item["bid"] = bid
                                    self.action(items=result_strategy.data)
                    else:
                        break
            if len(self.data[symbol])>1: 
                self.data[symbol] = self.data[symbol][self.data[symbol].index(row) + 1:]
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

    #--------------------------------------------- action
    def action(self, items:dict)-> model_output:
        #-------------- Variable
        output = model_output()
        #--------------Action
        for item in items :
            run = item.get("run")
            if run == Strategy_Run.ORDER_OPEN : output:model_output =self.order_open(item=item)
            if run == Strategy_Run.ORDER_CLOSE : output:model_output = self.order_close(item=item)
            if run == Strategy_Run.ORDER_CLOSE_ALL : output:model_output = self.order_close_all(item=item)
        #--------------Return
        return output
    
    #--------------------------------------------- check_tp_sl
    def check_tp_sl(self, symbol, ask, bid, date)-> model_output:
        #--------------Variable
        output = []
        #--------------Action
        for order in self.list_order_open :
            fire = False
            order_symbol = order[10]
            if order_symbol == symbol :
                #--------------Data
                id = order[0]
                price_open = order[5]
                action = order[11]
                amount = order[12]
                order_tp = order[13]
                order_sl = order[14]
                #--------------Variable
                #---Buy
                if action == "buy":
                    if bid > order_tp and order_tp > 0 : fire = True
                    if bid < order_sl and order_sl > 0 : fire = True
                #---Sell
                if action == "sell":
                    if ask < order_tp and order_tp > 0 :fire = True
                    if ask > order_sl and order_sl > 0 : fire = True
                #---Fire
                if fire :
                    item = {"id":id, "symbol":order_symbol, "action":action, "amount":amount, "price_open":price_open, "ask":ask, "bid":bid, "date":date}
                    output.append(item)
        #--------------Return
        return output

    #--------------------------------------------- check_limit
    def check_limit(self, ask, bid, date)-> model_output:
        #--------------Variable
        result = True
        param = None
        profit_close = 0
        profit_open = 0
        trade_count = 0
        #--------------Calculate
        for item in self.list_order_close : 
            trade_count += 1
            profit_close = profit_close + item[8]
            profit_close = float(f"{profit_close:.{2}f}")
        for item in self.list_order_open : 
            trade_count += 1
            profit_open = profit_open + self.profit_calculate(item, ask, bid)
            profit_open = float(f"{profit_open:.{2}f}")
        #--------------Trade
        if self.strategy.limit_trade !=-1 and trade_count >= self.strategy.limit_trade : 
            result = False
            param = 'trade'
        #--------------Profit
        if self.strategy.limit_profit !=-1 and profit_close >= self.strategy.limit_profit:
            result = False
            param='profit'
        #--------------Loss
        if profit_close < 0 :
            profit_open = profit_open + profit_close
            if self.strategy.limit_loss !=-1 and profit_open <= self.strategy.limit_loss:
                result = False
                param='loss'
        else:
            if self.strategy.limit_loss !=-1 and profit_open <= self.strategy.limit_loss:
                result = False
                param='loss'
        #--------------Log
        if (self.account_profit != profit_close or self.account_loss != profit_open):
            if (abs(profit_close-self.account_profit)>1 or abs(profit_open-self.account_loss)>1) :
                self.account_profit = profit_close
                self.account_loss = profit_open
                cmd = f"INSERT INTO back_execute_detaile (date,execute_id,step,profit,loss) VALUES('{date}', {self.execute_id}, {self.step}, {profit_close}, {profit_open})"
                self.management_sql.db.execute(cmd=cmd)
        #--------------Return
        output = result, param
        return output

    #--------------------------------------------- profit_calculate
    def profit_calculate(self, item, ask, bid)-> model_output:
        #--------------Data
        action = item[11]
        amount = item[12]
        price_open = item[5]
        profit = 0
        #--------------Action
        profit = (bid - price_open) * amount if action == "buy" else (price_open - ask) * amount if action == "sell" else 0
        profit = f"{profit:.{2}f}"
        #--------------Return
        output = float(profit)
        return output
    
    #--------------------------------------------- order_open
    def order_open(self, item:dict)-> model_output:
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
            #-------------- Data
            father_id = item.get("father_id")
            symbol = item.get("symbol")
            action = item.get("action")
            amount = item.get("amount")
            tp_pips = item.get("tp_pips")
            sl_pips = item.get("sl_pips")
            ask = item.get("ask")
            bid = item.get("bid")
            date = item.get("date")
            #-------------- TP/SL
            if tp_pips or sl_pips:
                point_size = list_instrument[symbol]["point_size"]
                digits = list_instrument[symbol]["digits"]
                if action == "buy":
                    price_open = ask
                    tp = float(f"{ask + tp_pips * point_size:.{digits}f}")
                    sl = float(f"{bid - sl_pips * point_size:.{digits}f}")
                elif action == "sell":
                    price_open = bid
                    tp = float(f"{bid - tp_pips * point_size:.{digits}f}")
                    sl = float(f"{ask + sl_pips * point_size:.{digits}f}")
            #-------------- Action
            obj = model_back_order_db()
            obj.father_id = father_id
            obj.date_open = date
            obj.execute_id = self.execute_id
            obj.step = self.step
            obj.symbol = symbol
            obj.action = action
            obj.amount = amount
            obj.bid = bid
            obj.ask = ask
            obj.price_open = price_open
            obj.tp = tp
            obj.sl = sl
            obj.status = 'open'
            result_database:model_output = self.management_orm.add(model=model_back_order_db, item=obj)
            #-------------- Orders
            self.list_order_open = self.management_sql.db.items(cmd=f"select * FROM back_order WHERE execute_id='{self.execute_id}' and step='{self.step}' AND status='open'").data
            self.list_order_close = self.management_sql.db.items(cmd=f"select * FROM back_order WHERE execute_id='{self.execute_id}' and step='{self.step}' AND status='close'").data
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.status = result_database.status
            output.data = None
            output.message = f"{symbol} | {action} | {amount} | {price_open} | {tp} | {sl}"
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
    def order_close(self, item:dict)-> model_output:
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
            #-------------- Data
            id = item.get("id")
            symbol = item.get("symbol")
            action = item.get("action")
            amount = item.get("amount")
            price_open = item.get("price_open")
            ask = item.get("ask")
            bid = item.get("bid")
            date= item.get("date")
            #-------------- Profit
            if action == "buy":
                price_close = bid
                profit = (bid - price_open) * amount
            elif action == "sell":
                price_close = ask
                profit = (price_open - ask) * amount
            profit = float(f"{profit:.{2}f}")
            self.account_profit = self.account_profit + profit
            item["profit"] = profit
            #-------------- Action
            cmd = f"UPDATE back_order SET date_close='{date}', price_close={price_close}, profit={profit}, status='close' WHERE id='{id}'"
            result_database:model_output = self.management_sql.db.execute(cmd=cmd)
            #-------------- Orders
            self.list_order_open = self.management_sql.db.items(cmd=f"select * FROM back_order WHERE execute_id='{self.execute_id}' and step='{self.step}' AND status='open'").data
            self.list_order_close = self.management_sql.db.items(cmd=f"select * FROM back_order WHERE execute_id='{self.execute_id}' and step='{self.step}' AND status='close'").data
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.status = result_database.status
            output.data = item
            output.message = f"{id} | {symbol} | {action} | {profit}"
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
    
    #--------------------------------------------- order_close_all
    def order_close_all(self, item:dict):
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
            price_open = item.get("price_open")
            ask = item.get("ask")
            bid = item.get("bid")
            date= item.get("date")
            #-------------- Action
            for order in self.list_order_open :
                id = order[0]
                symbol = order[10]
                action = order[11]
                amount = order[12]
                price_open = order[5]
                item = {"id":id, "symbol":symbol, "action":action, "amount":amount, "price_open":price_open, "ask":ask, "bid":bid, "date":date}
                self.order_close(item =item)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = None
            output.message = len(self.list_order_open)
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
    
    #--------------------------------------------- get_data
    def get_data(self, params):
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
            for item in params:
                symbol = item.get("symbol")
                date_from = item.get("date_from")
                date_to = item.get("date_to")
                table = get_tbl_name(symbol, "t1")
                cmd = f"SELECT id, date, ask, bid FROM {table} WHERE date>='{date_from}' and date<='{date_to}' ORDER BY date ASC"
                result:model_output = self.data_sql.db.items(cmd=cmd)
                if result.status == True :
                    output.data[symbol] = result.data
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
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
            cmd = f"SELECT max(count) FROM back_order WHERE execute_id={execute_id}"
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
            cmd = f"DELETE FROM back_order WHERE execute_id={execute_id}"
            self.management_sql.db.execute(cmd=cmd)
            cmd = f"DELETE FROM back_execute_detaile WHERE execute_id={execute_id}"
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
    
    #-------------------------- [order_detaile]
    def order_detaile(self, execute_id) -> model_output:
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
        detaile = []
        
        try:
            cmd = f"SELECT max(count) FROM back_order WHERE execute_id={execute_id}"
            max_count = self.management_sql.db.items(cmd=cmd).data[0][0]
            if max_count:
                #--------------All
                cmd = f"SELECT min(date_open), max(date_close), count(id), sum(profit) FROM back_order WHERE execute_id={execute_id}"
                data = self.management_sql.db.items(cmd=cmd).data[0]
                date_from = data[0].strftime('%Y-%m-%d %H:%M:%S')
                date_to = data[1].strftime('%Y-%m-%d %H:%M:%S')
                all_count = data[2]
                profit = f"{data[3]:.{2}f}"
                cmd = f"SELECT count(id) FROM back_order WHERE execute_id={execute_id} and status='open'"
                open_count = self.management_sql.db.items(cmd=cmd).data[0][0]
                cmd = f"SELECT count(id) FROM back_order WHERE execute_id={execute_id} and status='close'"
                close_count = self.management_sql.db.items(cmd=cmd).data[0][0]
                cmd = f"SELECT count(id) FROM back_order  WHERE execute_id={execute_id} and status='close'"
                close_count = self.management_sql.db.items(cmd=cmd).data[0][0]
                cmd = f"SELECT min(profit), max(profit), min(loss), max(loss) FROM back_execute_detaile WHERE execute_id={execute_id}"
                data = self.management_sql.db.items(cmd=cmd).data[0]
                profit_min = f"{data[0]:.{2}f}"
                profit_max = f"{data[1]:.{2}f}"
                loss_max = f"{data[2]:.{2}f}"
                loss_min = f"{data[3]:.{2}f}"
                detaile.append({
                    "count":'All',
                    "date_from":date_from,
                    "date_to":date_to,
                    "all_count":all_count,
                    "profit":profit,
                    "open_count":open_count,
                    "close_count":close_count,
                    "profit_min":profit_min,
                    "profit_max":profit_max,
                    "loss_min":loss_min,
                    "loss_max":loss_max
                })
                #--------------Items
                for i in range(max_count):
                    i += 1
                    cmd = f"SELECT min(date_open), max(date_close), count(id), sum(profit) FROM back_order WHERE execute_id={execute_id} and count={i}"
                    data = self.management_sql.db.items(cmd=cmd).data[0]
                    date_from = data[0].strftime('%Y-%m-%d %H:%M:%S')
                    date_to = data[1].strftime('%Y-%m-%d %H:%M:%S')
                    all_count = data[2]
                    profit = f"{data[3]:.{2}f}"
                    cmd = f"SELECT count(id) FROM back_order WHERE execute_id={execute_id} and count={i} and status='open'"
                    open_count = self.management_sql.db.items(cmd=cmd).data[0][0]
                    cmd = f"SELECT count(id) FROM back_order WHERE execute_id={execute_id} and count={i} and status='close'"
                    close_count = self.management_sql.db.items(cmd=cmd).data[0][0]
                    cmd = f"SELECT count(id) FROM back_order  WHERE execute_id={execute_id} and count={i} and status='close'"
                    close_count = self.management_sql.db.items(cmd=cmd).data[0][0]
                    cmd = f"SELECT min(profit), max(profit), min(loss), max(loss) FROM back_execute_detaile WHERE execute_id={execute_id} and count={i}"
                    data = self.management_sql.db.items(cmd=cmd).data[0]
                    profit_min = f"{data[0]:.{2}f}"
                    profit_max = f"{data[1]:.{2}f}"
                    loss_max = f"{data[2]:.{2}f}"
                    loss_min = f"{data[3]:.{2}f}"
                    detaile.append({
                        "count":i,
                        "date_from":date_from,
                        "date_to":date_to,
                        "all_count":all_count,
                        "profit":profit,
                        "open_count":open_count,
                        "close_count":close_count,
                        "profit_min":profit_min,
                        "profit_max":profit_max,
                        "loss_min":loss_min,
                        "loss_max":loss_max
                    })
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = detaile
            output.message=execute_id
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
        table = "back_execute"
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
        table1 = "back_execute" 
        table2 = "back_order"
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
    