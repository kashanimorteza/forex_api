#--------------------------------------------------------------------------------- Location
# myLib/logic_backtest.py

#--------------------------------------------------------------------------------- Description
# logic_backtest

#--------------------------------------------------------------------------------- Import
import inspect, time, ast
from myLib.logic_global import debug, list_instrument, log_instance, data_instance, Strategy_Run
from myLib.utils import model_output, sort, get_tbl_name
from myLib.log import Log
from myLib.data_sql import Data_SQL
from myLib.data_orm import Data_Orm
from myLib.logic_management import Logic_Management
from myModel.model_back_order import model_back_order_db

#--------------------------------------------------------------------------------- Action
class Logic_BackTest:
    #--------------------------------------------- init
    def __init__(self, execute_id, data_sql:Data_SQL=None, management_sql:Data_SQL=None, management_orm:Data_Orm=None, log:Log=None):
        #--------------------Variable
        self.this_class = self.__class__.__name__
        self.execute_id = execute_id
        self.strategy = None
        self.data = None
        self.list_order_open = []
        self.list_order_close = []
        #--------------------Instance
        self.management_orm = management_orm if management_orm else data_instance["management_orm"]
        self.management_sql = management_sql if management_sql else data_instance["management_sql"]
        self.data_sql = data_sql if data_sql else data_instance["data_sql"]
        self.log = log if log else log_instance
        self.logic_management = Logic_Management()

    #--------------------------------------------- run
    def run(self):
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
            self.strategy_name = detaile.get("strategy_name")
            self.status = detaile.get("status")
            self.date_from = detaile.get("date_from")
            self.date_to = detaile.get("date_to")
            self.params = ast.literal_eval(detaile.get("params"))
            #--------------Data
            self.symbols = self.params.get("symbols", "").split(',')
            self.data = self.get_data(symbols=self.symbols, date_from=self.date_from, date_to=self.date_to).data
            #--------------Strategy
            self.strategy = self.logic_management.get_strategy_instance(self.strategy_name, self.params).data
            #--------------Start
            result_start:model_output = self.start()
            #--------------Next
            result_next:model_output = self.next()
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.message = f"{result_start.status} | {result_next.status}"
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

    #--------------------------------------------- strategy_start
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
            #--------------Data
            result_strategy: model_output = self.strategy.start()
            #--------------Items
            for item in result_strategy.data :
                item["father_id"] = 0
                item["date"] = self.data[item.get("symbol")][0][1]
                item["ask"] = self.data[item.get("symbol")][0][2]
                item["bid"] = self.data[item.get("symbol")][0][3]
            self.data[item.get("symbol")].pop(0)
            state = item.get("state")
            #--------------Action
            result_action:model_output = self.action(items=result_strategy.data)
            #--------------Database
            cmd = f"UPDATE back_execute SET status='{state}' WHERE id={self.execute_id}"
            result_database:model_output = self.management_sql.db.execute(cmd=cmd)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = None
            output.message = f"{result_strategy.status} | {result_action.status} | {result_database.status}"
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
                    id = row[0]
                    date = row[1]
                    ask = row[2]
                    bid = row[3]
                    #---Check TP/SL
                    fires = self.check_tp_sl(symbol=symbol, ask=ask, bid=bid, date=date)
                    for item in fires :
                        self.order_close(item =item)
                        if order_open_accept:
                            order_id = item.get("id")
                            order_detaile = self.logic_management.order_detaile(order_id=order_id, mode="back").data
                            result_strategy:model_output = self.strategy.order_close(order_detaile=order_detaile)
                            for item in result_strategy.data :
                                item["father_id"] = order_id
                                item["date"] = date
                                item["ask"] = ask
                                item["bid"] = bid
                                self.action(items=result_strategy.data)
                    #---Check limit
                    check_limit_status, check_limit_param  = self.check_limit(ask, bid)
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
                cmd = f"SELECT id, date, ask, bid FROM {table} WHERE date>='{date_from}' and date<='{date_to}' ORDER BY date ASC"
                result:model_output = self.data_sql.db.items(cmd=cmd)
                if result.status == True :
                    output.data[symbol] = result.data
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.message = f"{date_from} | {date_to} | {len(symbols)}"
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
            for item in items :
                run = item.get("run")
                if run == Strategy_Run.ORDER_OPEN : result:model_output =self.order_open(item=item)
                if run == Strategy_Run.ORDER_CLOSE : result:model_output = self.order_close(item=item)
                if run == Strategy_Run.ORDER_CLOSE_ALL : result:model_output = self.order_close_all(item=item)
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

    #--------------------------------------------- check_tp_sl
    def check_tp_sl(self, symbol, ask, bid, date)-> model_output:
        #--------------Variable
        items = []
        #--------------Action
        for order in self.list_order_open :
            fire = False
            order_symbol = order[6]
            if order_symbol == symbol :
                order_id = order[0]
                order_action = order[7]
                order_amount = order[8]
                price_open = order[11]
                order_tp = order[13]
                order_sl = order[14]
                #--------------Check TP/SL
                #---Buy
                if order_action == "buy":
                    if bid > order_tp and order_tp > 0 : fire = True
                    if bid < order_sl and order_sl > 0 : fire = True
                #---Sell
                if order_action == "sell":
                    if ask < order_tp and order_tp > 0 :fire = True
                    if ask > order_sl and order_sl > 0 : fire = True
                #---Fire
                if fire :
                    item = {"id":order_id, "symbol":order_symbol, "action":order_action, "amount":order_amount, "price_open":price_open, "ask":ask, "bid":bid, "date":date}
                    items.append(item)
        #--------------Return
        return items

    #--------------------------------------------- check_limit
    def check_limit(self, ask, bid)-> model_output:
        #--------------Variable
        result = True
        param = None
        profit_close = 0
        profit_open = 0
        trade_count = 0
        #--------------Calculate
        for item in self.list_order_close : 
            trade_count += 1
            profit_close = profit_close + item[15]
        for item in self.list_order_open : 
            trade_count += 1
            profit_open = profit_open + self.profit_calculate(item, ask, bid)
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
            if self.strategy.limit_loss !=-1 and (profit_open+profit_close) <= self.strategy.limit_loss:
                result = False
                param='loss'
        else:
            if self.strategy.limit_loss !=-1 and profit_open <= self.strategy.limit_loss:
                result = False
                param='loss'
        #--------------Return
        output = result, param
        return output

    #--------------------------------------------- profit_calculate
    def profit_calculate(self, item, ask, bid)-> model_output:
        #--------------Data
        action = item[7]
        amount = item[8]
        price_open = item[11]
        #--------------Action
        if action == "buy":
            profit = (bid - price_open) * amount
        elif action == "sell":
            profit = (price_open - ask) * amount
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
            self.list_order_open = self.management_sql.db.items(cmd=f"select * FROM back_order WHERE execute_id='{self.execute_id}' AND status='open'").data
            self.list_order_close = self.management_sql.db.items(cmd=f"select * FROM back_order WHERE execute_id='{self.execute_id}' AND status='close'").data
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
            profit = f"{profit:.{2}f}"
            #-------------- Action
            cmd = f"UPDATE back_order SET date_close='{date}', price_close={price_close}, profit={profit}, status='close' WHERE id='{id}'"
            result_database:model_output = self.management_sql.db.execute(cmd=cmd)
            #-------------- Orders
            self.list_order_open = self.management_sql.db.items(cmd=f"select * FROM back_order WHERE execute_id='{self.execute_id}' AND status='open'").data
            self.list_order_close = self.management_sql.db.items(cmd=f"select * FROM back_order WHERE execute_id='{self.execute_id}' AND status='close'").data
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.status = result_database.status
            output.data = None
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
                order_symbol = order[6]
                order_id = order[0]
                order_action = order[7]
                order_amount = order[8]
                price_open = order[11]
                item = {"id":order_id, "symbol":order_symbol, "action":order_action, "amount":order_amount, "price_open":price_open, "ask":ask, "bid":bid, "date":date}
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