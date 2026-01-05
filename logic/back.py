#--------------------------------------------------------------------------------- Location
# logic/logic_back.py

#--------------------------------------------------------------------------------- Description
# logic_back

#--------------------------------------------------------------------------------- Import
import inspect, time, ast
from logic.startup import Strategy_Action, Strategy_Run, debug, list_instrument, log_instance, database_management, database_data
from logic.util import model_output, sort, get_tbl_name, time_change_utc_newyork, cal_price_pips, cal_size, cal_tp_sl, cal_movement, cal_percent_of_value, cal_value_of_percent, cal_profit
from logic.log import Logic_Log
from logic.data_sql import Data_SQL
from logic.data_orm import Data_Orm
from model.back_order import model_back_order_db
from strategy import *
from model import *

#--------------------------------------------------------------------------------- Action
class Logic_Back:
    #--------------------------------------------- init
    def __init__(
            self, 
            execute_id=None,
            management_sql:Data_SQL=None, 
            management_orm:Data_Orm=None, 
            data_sql:Data_SQL=None, 
            log:Logic_Log=None
        ):
        #-------------- Debug
        self.this_class = self.__class__.__name__
        #-------------- Variable
        self.execute_id = execute_id
        #-------------- Instance
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
        #-------------- Action
        try:
            #------execute_detaile
            ed:model_output = self.execute_detaile(id=self.execute_id)
            strategy_name = ed["strategy_name"]
            symbols = ed["symbols"].split(',')
            step = ed["step"]
            profit_manager_id = ed["profit_manager_id"]
            money_management_id = ed["money_management_id"]
            self.date_from = ed["date_from"]
            self.date_to = ed["date_to"]
            self.tp_pips = ed["tp_pips"]
            self.sl_pips = ed["sl_pips"]
            #------Strategy
            self.strategy = self.get_strategy_instance(strategy_name, ed).data
            #------Step and Date
            cmd = f"SELECT MAX(step),max(date_close) FROM back_order WHERE execute_id={self.execute_id}"
            data = self.management_sql.db.items(cmd=cmd).data
            if data[0][0]:
                self.step = data[0][0]+1
                self.date_from = data[0][1]
            else:
                self.step = 1
            #------Data
            data_params = []
            for symbol in symbols : data_params.append({"symbol": symbol, "date_from":self.date_from, "date_to": self.date_to})
            self.data = self.get_data(params=data_params).data
            #------profit_manager
            cmd = f"SELECT * FROM profit_manager_item WHERE profit_manager_id={profit_manager_id} ORDER BY value DESC"
            self.profit_manager_items = self.management_sql.db.items(cmd=cmd).data 
            #------money_management
            cmd = f"SELECT balance, risk, limit_profit, limit_loss, limit_trade FROM money_management WHERE id={money_management_id}"
            self.money_management = self.management_sql.db.items(cmd=cmd).data[0]
            #------Do
            for i in range(step):
                #---Rest
                self.strategy.balance = self.money_management[0]
                self.strategy.risk = self.money_management[1]
                self.strategy.limit_profit = self.money_management[2]
                self.strategy.limit_loss = self.money_management[3]
                self.strategy.limit_trade = self.money_management[4]
                self.account_balance = self.money_management[0]
                self.account_profit_close = 0
                self.account_profit_open = 0
                self.list_order_open = []
                self.list_order_close = []
                self.list_order_pending = []
                #---Start
                result_start:model_output = self.start()
                #---Next
                result_next:model_output = self.next()
                #---Stop
                result_stop:model_output = self.stop()
                #---Step
                self.step += 1
            #------Database
            cmd = f"UPDATE back_execute SET status='stop' WHERE id={self.execute_id}"
            result_database:model_output = self.management_sql.db.execute(cmd=cmd)
        except Exception as e:  
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #------Output
        output.time = sort(f"{(time.time() - start_time):.3f}", 3)
        output.data = None
        output.message = f"{self.execute_id} | {strategy_name} | {symbols} | {step} | {result_start.status} | {result_next.status} | {result_database.status} | {result_stop.status}"
        #------Verbose
        if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
        #------Log
        if log : self.log.log(log_model, output)
        #--------------Return
        return output

    #--------------------------------------------- start
    def start(self):
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
        #-------------- Action
        try:
            #------Data
            result_strategy:model_output = self.strategy.start()
            #------Items
            if result_strategy.status :
                for item in result_strategy.data :
                    symbol = item.get("symbol")
                    if len(self.data[symbol])>0:
                        item["father_id"] = 0
                        item["date"] = self.data[symbol][0][1]
                        item["ask"] = self.data[symbol][0][2]
                        item["bid"] = self.data[symbol][0][3]
                        self.data[symbol].pop(0)
                    else:
                        result_strategy.data.remove(item)
            #------Action
            result_action:model_output = self.action(items=result_strategy.data)
            #------Database
            cmd = f"UPDATE back_execute SET status='{Strategy_Action.START}' WHERE id={self.execute_id}"
            result_database:model_output = self.management_sql.db.execute(cmd=cmd)
        except Exception as e:  
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #------Output
        output.time = sort(f"{(time.time() - start_time):.3f}", 3)
        output.data = None
        output.message = f"{self.execute_id} | {result_strategy.status} | {result_action.status} | {result_database.status}"
        #------Verbose
        if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
        #------Log
        if log : self.log.log(log_model, output)
        #--------------Return
        return output

    #--------------------------------------------- stop
    def stop(self):
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
        #-------------- Action
        try:
            #------Data
            result_strategy:model_output = self.strategy.stop()
            #------Action
            result_action:model_output = self.action(items=result_strategy.data)
            #------Database
            cmd = f"UPDATE back_execute SET status='{Strategy_Action.STOP}' WHERE id={self.execute_id}"
            result_database:model_output = self.management_sql.db.execute(cmd=cmd)
        except Exception as e:  
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #------Output
        output.time = sort(f"{(time.time() - start_time):.3f}", 3)
        output.data = None
        output.message = f"{self.execute_id} | {result_strategy.status} | {result_action.status} | {result_database.status}"
        #------Verbose
        if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
        #------Log
        if log : self.log.log(log_model, output)
        #--------------Return
        return output
    
    #--------------------------------------------- next
    def next(self):
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
        result = model_output()
        output.class_name = self.this_class
        output.method_name = this_method
        #-------------- Variable
        self.order_open_accept = True
        self.price_data = {}
        check_tp_sls = []
        #--------------Action
        try:
            for symbol in self.data:
                self.digits = list_instrument[symbol]["digits"]
                self.point_size = list_instrument[symbol]["point_size"]
                for row in self.data[symbol]:
                    #------price_data
                    date = row[1]
                    ask = float(row[2])
                    bid = float(row[3])
                    self.price_data[symbol]={'digits': self.digits, 'point_size': self.point_size, 'date': date, 'ask': ask, 'bid': bid}
                    #------check_pending_order
                    if len(self.list_order_pending)>0 :
                        self.check_pending_order(self.price_data)
                    #------profit_manager
                    if len(self.list_order_open)>0 : 
                        self.profit_manager(self.price_data)
                    #------check_tp_sl
                    if len(self.list_order_open)>0 : 
                        check_tp_sls = self.check_tp_sl(symbol=symbol, ask=ask, bid=bid, date=date)
                    #------check_limit
                    self.check_limit(ask, bid, date, self.digits, self.point_size)
                    #------order_close
                    if self.order_open_accept:
                        for check_tp_sl in check_tp_sls :
                            result_strategy:model_output = self.strategy.order_close(order_detaile=check_tp_sl)
                            for item in result_strategy.data :
                                item["father_id"] = check_tp_sl.get("id")
                                item["date"] = date
                                item["ask"] = ask
                                item["bid"] = bid
                                self.action(items=result_strategy.data)
                    #------Price_change
                    result_strategy_price_change:model_output = self.strategy.price_change(
                        price_data=self.price_data,
                        order_close=self.order_close,
                        order_open=self.order_open,
                        order_pending=self.order_pending
                    )
                    if result_strategy_price_change.status:
                        for item in result_strategy_price_change.data :
                            item["father_id"] = -1
                            item["state"] = Strategy_Action.PRICE_CHANGE
                        self.action(items=result_strategy_price_change.data)
                if len(self.data[symbol])>1 : 
                    self.data[symbol] = self.data[symbol][self.data[symbol].index(row) + 1:]
        except Exception as e:  
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Output
        output = result
        output.time = sort(f"{(time.time() - start_time):.3f}", 3)
        #--------------Verbose
        if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
        #--------------Log
        if log : self.log.log(log_model, output)
        #--------------Return
        return output

    #--------------------------------------------- profit_manager
    def profit_manager(self, price_data:dict)-> model_output:
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
        output.data = []
        execute = False
        #-------------- Action
        try:
            for item in price_data:
                #------Data
                symbol = item
                digits = price_data[symbol]['digits']
                point_size = price_data[symbol]['point_size']
                date = price_data[symbol]['date']
                ask = price_data[symbol]['ask']
                bid = price_data[symbol]['bid']
                #------Check
                for order_open in self.list_order_open:
                    order_symbol = order_open[10]
                    if symbol == order_symbol :
                        #---Order
                        order_id = order_open[0]
                        order_price_open = order_open[5]
                        order_action = order_open[11]
                        order_price_tp = order_open[13]
                        order_price_sl = order_open[14]
                        order_pm = order_open[16]
                        #---Trend
                        movement = cal_movement(order_action, order_price_open, ask, bid, digits, point_size)
                        #---PM
                        if movement>0:
                            for pm in self.profit_manager_items:
                                if pm[2] == order_pm : break
                                value = pm[3]
                                tp_value = pm[4]
                                sl_value = pm[5]
                                percent = cal_percent_of_value(self.tp_pips, movement)
                                if percent >= value:
                                    if tp_value and abs(tp_value)>0:
                                        pips = cal_value_of_percent(self.tp_pips, abs(tp_value), digits, point_size)
                                        if tp_value>0:
                                            if order_action == "buy":
                                                tp = cal_price_pips(order_price_tp, pips, digits, point_size)
                                            else:
                                                tp = cal_price_pips(order_price_tp, -pips, digits, point_size)
                                        else:
                                            if order_action == "buy":
                                                tp = cal_price_pips(order_price_tp, -pips, digits, point_size)
                                            else:
                                                tp = cal_price_pips(order_price_tp, +pips, digits, point_size)
                                        cmd = f"UPDATE back_order SET tp={tp}, profit_manager='{pm[2]}' WHERE id={order_id}"
                                        self.management_sql.db.execute(cmd=cmd)
                                        cmd = f"INSERT INTO back_profit_manager_detaile (date, order_id, ask, bid, execute, value) VALUES('{date}', {order_id}, {ask}, {bid}, 'TP', {tp})"
                                        self.management_sql.db.execute(cmd=cmd)
                                        message = f"{date} | {symbol} | {sort(order_action, 4)} | {order_id} | {pm[2]} | TP | old({order_price_tp}) | {pips} | new({tp})"
                                        output.time = sort(f"{(time.time() - start_time):.3f}", 3)
                                        self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", message)
                                        execute = True
                                    if sl_value and abs(sl_value)>0:
                                        pips = cal_value_of_percent(self.sl_pips, abs(sl_value), digits, point_size)
                                        if sl_value>0:
                                            if order_action == "buy":
                                                sl = cal_price_pips(order_price_sl, -pips, digits, point_size)
                                            else:
                                                sl = cal_price_pips(order_price_sl, pips, digits, point_size)
                                        else:
                                            if order_action == "buy":
                                                sl = cal_price_pips(order_price_sl, pips, digits, point_size)
                                            else:
                                                sl = cal_price_pips(order_price_sl, -pips, digits, point_size)
                                        cmd = f"UPDATE back_order SET sl={sl}, profit_manager='{pm[2]}' WHERE id={order_id}"
                                        self.management_sql.db.execute(cmd=cmd)
                                        cmd = f"INSERT INTO back_profit_manager_detaile (date, order_id, ask, bid, execute, value) VALUES('{date}', {order_id}, {ask}, {bid}, 'SL', {sl})"
                                        self.management_sql.db.execute(cmd=cmd)
                                        message = f"{date} | {symbol} | {sort(order_action, 4)} | {order_id} | {pm[2]} | SL | old({order_price_sl}) | {pips} | new({sl})"
                                        output.time = sort(f"{(time.time() - start_time):.3f}", 3)
                                        self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", message)
                                        execute = True
                                    if execute:
                                        self.list_order_open = self.management_sql.db.items(cmd=f"select * FROM back_order WHERE execute_id={self.execute_id} and step={self.step} AND status='open'").data
                                        break
        except Exception as e:  
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Output
        output.time = sort(f"{(time.time() - start_time):.3f}", 3)
        output.message =  f"{date} | {len(output.data)}"
        #--------------Verbose
        if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
        #--------------Log
        if log : self.log.log(log_model, output)
        #--------------Return
        return output

    #--------------------------------------------- check_pending_order
    def check_pending_order(self, items:dict)-> model_output:
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
        output.data = []
        #-------------- Action
        try:
            for item in items:
                #------Data
                symbol = item
                date = items[symbol]['date']
                ask = items[symbol]['ask']
                bid = items[symbol]['bid']
                #------Check
                for order in self.list_order_pending:
                    order_date = order["date"]
                    order_action = order["action"]
                    order_price = order["price"]
                    order_amount = order["amount"]
                    pending_limit = order["pending_limit"]
                    if (date - order_date).seconds <= pending_limit:
                        if order_action=="buy":
                            if ask>= order_price:
                                order["date"]=date
                                order["ask"]=ask
                                order["bid"]=bid
                                output.time = sort(f"{(time.time() - start_time):.3f}", 3)
                                message = f"{date} | {symbol} | {sort(order_action, 4)} | amt({order_amount}) | prc({order_price}) | prc({ask}) | Active"
                                self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", message)
                                output.data.append(order)
                                self.order_open(order)
                                self.list_order_pending.remove(order)
                        if order_action =="sell":
                            if bid<= order_price:
                                order["date"]=date
                                order["ask"]=ask
                                order["bid"]=bid
                                output.time = sort(f"{(time.time() - start_time):.3f}", 3)
                                message = f"{date} | {symbol} | {sort(order_action, 4)} | amt({order_amount}) | prc({order_price}) | prc({bid}) | Active"
                                self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", message)
                                output.data.append(order)
                                self.order_open(order)
                                self.list_order_pending.remove(order)
                    else:
                        self.list_order_pending.remove(order)
        except Exception as e:  
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Output
        output.time = sort(f"{(time.time() - start_time):.3f}", 3)
        output.message = f"{date} | {len(output.data)}"
        #--------------Verbose
        if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
        #--------------Log
        if log : self.log.log(log_model, output)
        #--------------Return
        return output

    #--------------------------------------------- check_limit
    def check_limit(self, ask, bid, date, digits, point_size)-> model_output:
        #--------------Variable
        result = True
        param = None
        profit_close = 0
        profit_open = 0
        trade_count = 0
        loss = 0
        #--------------check close order
        for item in self.list_order_close : 
            trade_count += 1
            profit_close = profit_close + item[8]
            profit_close = float(f"{profit_close:.{2}f}")
        #--------------check open order
        for item in self.list_order_open : 
            price_open = item[5]
            action = item[11]
            amount = item[12]
            trade_count += 1
            profit_open = profit_open + cal_profit(action, amount, price_open, ask, bid, digits, point_size)[0]
            profit_open = float(f"{profit_open:.{2}f}")
        #--------------Trade
        if self.strategy.limit_trade !=-1 and trade_count >= self.strategy.limit_trade : 
            result = False
            param = 'trade'
            self.order_open_accept = False
        #--------------Profit
        if self.strategy.limit_profit !=-1 and profit_close >= self.strategy.limit_profit:
            result = False
            param='profit'
            self.order_open_accept = False
        #--------------Loss
        loss = profit_open + profit_close
        if self.strategy.limit_loss !=-1 and loss<0 and loss <= self.strategy.limit_loss:
            result = False
            param='loss'
            self.order_open_accept = False
            result_strategy:model_output = self.strategy.stop()
            for item in result_strategy.data :
                item["date"] = date
                item["ask"] = ask
                item["bid"] = bid
                self.action(items=result_strategy.data)
        #--------------Log
        if not result: 
            p = f"{param} | {date}"
            cmd = f"INSERT INTO back_execute_detaile (date, execute_id, step, profit_close, profit_open, param) VALUES('{date}', {self.execute_id}, {self.step}, {profit_close}, {profit_open}, '{p}')"
            self.management_sql.db.execute(cmd=cmd)
        if (self.account_profit_close != profit_close or self.account_profit_open != profit_open):
            if (abs(profit_close-self.account_profit_close)>1 or abs(profit_open-self.account_profit_open)>1) :
                self.account_profit_close = profit_close
                self.account_profit_open = profit_open
                cmd = f"INSERT INTO back_execute_detaile (date, execute_id, step, profit_close, profit_open) VALUES('{date}', {self.execute_id}, {self.step}, {profit_close}, {profit_open})"
                self.management_sql.db.execute(cmd=cmd)
        #--------------Return
        output = result, param
        return output
    
    #--------------------------------------------- action
    def action(self, items:dict)-> model_output:
        #-------------- Variable
        output = model_output()
        #--------------Action
        for item in items :
            run = item["run"]
            if run == Strategy_Run.ORDER_OPEN : output:model_output =self.order_open(item=item)
            if run == Strategy_Run.ORDER_PENDING : output:model_output =self.order_pending(item=item)
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
                #------Data
                id = order[0]
                price_open = order[5]
                action = order[11]
                amount = order[12]
                order_tp = order[13]
                order_sl = order[14]
                #------Check Buy
                if action == "buy":
                    if bid > order_tp and order_tp > 0 : fire = True
                    if bid < order_sl and order_sl > 0 : fire = True
                #------Check Sell
                if action == "sell":
                    if ask < order_tp and order_tp > 0 :fire = True
                    if ask > order_sl and order_sl > 0 : fire = True
                #------Fire
                if fire :
                    item = {"id":id, "symbol":order_symbol, "action":action, "amount":amount, "price_open":price_open, "ask":ask, "bid":bid, "date":date}
                    result = self.order_close(item=item).data
                    profit =  result["profit"]
                    output.append(result)
                    self.account_profit_close = self.account_profit_close + profit
                    self.account_balance = self.account_balance + profit
                    self.strategy.balance = self.account_balance
        #-------------- Update
        if fire:
            self.list_order_open = self.management_sql.db.items(cmd=f"select * FROM back_order WHERE execute_id='{self.execute_id}' and step='{self.step}' AND status='open'").data
            self.list_order_close = self.management_sql.db.items(cmd=f"select * FROM back_order WHERE execute_id='{self.execute_id}' and step='{self.step}' AND status='close'").data
        #--------------Return
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
            digits = item.get("digits")
            point_size = item.get("point_size")
            #-------------- TP/SL
            price_open, tp, sl, spread = cal_tp_sl(action, ask, bid, tp_pips, sl_pips, digits, point_size)
            #-------------- Action
            obj = model_back_order_db()
            obj.father_id = father_id
            obj.date_open = date
            obj.execute_id = self.execute_id
            obj.step = self.step
            obj.symbol = symbol
            obj.action = action
            obj.amount = amount
            obj.price_open = price_open
            obj.tp = tp
            obj.sl = sl
            obj.spread = spread
            obj.profit_manager = ''
            obj.ask = ask
            obj.bid = bid
            obj.status = 'open'
            result_database:model_output = self.management_orm.add(model=model_back_order_db, item=obj)
            #-------------- Orders
            self.list_order_open = self.management_sql.db.items(cmd=f"select * FROM back_order WHERE execute_id='{self.execute_id}' and step='{self.step}' AND status='open'").data
            self.list_order_close = self.management_sql.db.items(cmd=f"select * FROM back_order WHERE execute_id='{self.execute_id}' and step='{self.step}' AND status='close'").data
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.status = result_database.status
            output.data = None
            output.message = f"{date} | {symbol} | {sort(action, 4)} | amt({amount}) | prc({price_open}) | tpt({tp}) | sls({sl})"
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
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

    #--------------------------------------------- order_pending
    def order_pending(self, item:dict)-> model_output:
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
        #-------------- Action
        try:
            self.list_order_pending.append(item)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = item
            if item['action']=="buy":
                output.time = sort(f"{(time.time() - start_time):.3f}", 3)
                message = f"{item['date']} | {item['symbol']} | {sort(item['action'], 4)} | amt({item['amount']}) | prc({item['price']}) | tp({item['tp_pips']}) | sp({item['sl_pips']}) | pl({item['pending_limit']}) | Placed"
                self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", message)
            else:
                output.time = sort(f"{(time.time() - start_time):.3f}", 3)
                message = f"{item['date']} | {item['symbol']} | {sort(item['action'], 4)} | amt({item['amount']}) | prc({item['price']}) | tp({item['tp_pips']}) | sp({item['sl_pips']}) | pl({item['pending_limit']}) | Placed"
                self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", message)
        except Exception as e:  
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Verbose
        if verbose and output.message  : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
        #--------------Log
        if log : self.log.log(log_model, output)
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
        #-------------- Action
        try:
            #------ Data
            id = item.get("id")
            symbol = item.get("symbol")
            action = item.get("action")
            amount = item.get("amount")
            price_open = item.get("price_open")
            ask = item.get("ask")
            bid = item.get("bid")
            date= item.get("date")
            digits = item.get("digits")
            point_size = item.get("point_size")
            #------ Profit
            profit, price_close = cal_profit(action, amount, price_open, ask, bid, digits, point_size)
            item["profit"] = profit
            item["price_close"] = price_close
            item["date_close"] = date
            item["status"] = 'close'
            #------ Database
            cmd = f"UPDATE back_order SET date_close='{date}', price_close={price_close}, profit={profit}, status='close' WHERE id='{id}'"
            result_database:model_output = self.management_sql.db.execute(cmd=cmd)
        except Exception as e:  
            #--------------Error
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Output
        output.time = sort(f"{(time.time() - start_time):.3f}", 3)
        output.status = result_database.status
        output.data = item
        output.message = f"{date} | {symbol} | {sort(action, 4)} | amt({amount}) | prc({price_close}) | prf({profit})"
        #--------------Verbose
        if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
        #--------------Log
        if log : self.log.log(log_model, output)
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
        #-------------- Action
        try:
            #------Data
            price_open = item.get("price_open")
            ask = item.get("ask")
            bid = item.get("bid")
            date= item.get("date")
            #------Action
            for order in self.list_order_open :
                id = order[0]
                symbol = order[10]
                action = order[11]
                amount = order[12]
                price_open = order[5]
                item = {"id":id, "symbol":symbol, "action":action, "amount":amount, "price_open":price_open, "ask":ask, "bid":bid, "date":date}
                self.order_close(item =item)
        except Exception as e:  
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Output
        output.time = sort(f"{(time.time() - start_time):.3f}", 3)
        output.data = None
        output.message = len(self.list_order_open)
        #--------------Verbose
        if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
        #--------------Log
        if log : self.log.log(log_model, output)
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
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
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
    
    #-------------------------- [order_step]
    def order_step(self, execute_id) -> model_output:
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
            cmd = f"SELECT max(step) FROM back_order WHERE execute_id={execute_id}"
            max_step = self.management_sql.db.items(cmd=cmd).data[0][0]
            if max_step is None : max_step = 0
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = max_step
            output.message=max_step
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
            #--------------Log
            if log : self.log.log(log_model, output)
        except Exception as e:  
            #--------------Error
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Return
        return max_step

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
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
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
    
    #-------------------------- [order_truncate]
    def order_truncate(self) -> model_output:
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
            self.management_orm.truncate_all_table()
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = None
            output.message=None
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
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
    
    #-------------------------- [action_detaile]
    def action_detaile(self, execute_id) -> model_output:
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
            cmd = f"SELECT max(step) FROM back_order WHERE execute_id={execute_id}"
            max_step = self.management_sql.db.items(cmd=cmd).data[0][0]
            if max_step:
                #--------------All
                cmd = f"SELECT min(date_open), max(date_close), count(id), sum(profit) FROM back_order WHERE execute_id={execute_id}"
                data = self.management_sql.db.items(cmd=cmd).data[0]
                date_from = data[0].strftime('%Y-%m-%d %H:%M:%S')
                date_to = data[1].strftime('%Y-%m-%d %H:%M:%S')
                trade_all = data[2]
                profit_all = data[3]
                #--------------Profit
                cmd = f"SELECT sum(profit) FROM back_order WHERE execute_id={execute_id} and profit>0"
                profit_positive = self.management_sql.db.items(cmd=cmd).data[0][0]
                if not profit_positive : profit_positive = 0
                cmd = f"SELECT sum(profit) FROM back_order WHERE execute_id={execute_id} and profit<0"
                profit_negative = self.management_sql.db.items(cmd=cmd).data[0][0]
                if not profit_negative : profit_negative = 0
                #--------------Trade: open/close
                cmd = f"SELECT count(id) FROM back_order WHERE execute_id={execute_id} and status='open'"
                trade_open = self.management_sql.db.items(cmd=cmd).data[0][0]
                cmd = f"SELECT count(id) FROM back_order WHERE execute_id={execute_id} and status='close'"
                trade_close = self.management_sql.db.items(cmd=cmd).data[0][0]
                #--------------Trade: sell/buy
                cmd = f"SELECT count(id) FROM back_order WHERE execute_id={execute_id} and action='buy'"
                trade_buy = self.management_sql.db.items(cmd=cmd).data[0][0]
                cmd = f"SELECT count(id) FROM back_order WHERE execute_id={execute_id} and action='sell'"
                trade_sell = self.management_sql.db.items(cmd=cmd).data[0][0]
                #--------------Detaile
                cmd = f"SELECT min(profit_close), max(profit_close), max(profit_open), min(profit_open) FROM back_execute_detaile WHERE execute_id={execute_id}"
                data = self.management_sql.db.items(cmd=cmd).data[0]
                profit_close_min = data[0]
                profit_close_max = data[1]
                profit_open_min = data[2]
                profit_open_max=data[3]
                #--------------Param
                param = f""
                #--------------Add
                detaile.append({
                    "step":'All',
                    "date_from":date_from,
                    "date_to":date_to,
                    "trade_all":f"{trade_all}",
                    "trade_open":f"{trade_open}",
                    "trade_close":f"{trade_close}",
                    "trade_buy":f"{trade_buy}",
                    "trade_sell":f"{trade_sell}",
                    "profit_all":f"{profit_all:.{2}f}",
                    "profit_positive":f"{profit_positive:.{2}f}",
                    "profit_negative":f"{profit_negative:.{2}f}",
                    "profit_close_min":f"{profit_close_min:.{2}f}",
                    "profit_close_max":f"{profit_close_max:.{2}f}",
                    "profit_open_min":f"{profit_open_min:.{2}f}",
                    "profit_open_max":f"{profit_open_max:.{2}f}",
                    "param":param
                })
                #--------------Items
                for i in range(max_step):
                    i += 1
                    #--------------All
                    cmd = f"SELECT min(date_open), max(date_close), count(id), sum(profit) FROM back_order WHERE execute_id={execute_id} and step={i}"
                    data = self.management_sql.db.items(cmd=cmd).data[0]
                    date_from = data[0].strftime('%Y-%m-%d %H:%M:%S')
                    date_to = data[1].strftime('%Y-%m-%d %H:%M:%S')
                    trade_all = data[2]
                    profit_all = data[3]
                    #--------------Profit
                    cmd = f"SELECT sum(profit) FROM back_order WHERE execute_id={execute_id} and profit>0 and step={i}"
                    profit_positive = self.management_sql.db.items(cmd=cmd).data[0][0]
                    if not profit_positive : profit_positive = 0
                    cmd = f"SELECT sum(profit) FROM back_order WHERE execute_id={execute_id} and profit<0 and step={i}"
                    profit_negative = self.management_sql.db.items(cmd=cmd).data[0][0]
                    if not profit_negative : profit_negative = 0
                    #--------------Trade: open/close
                    cmd = f"SELECT count(id) FROM back_order WHERE execute_id={execute_id} and status='open' and step={i}"
                    trade_open = self.management_sql.db.items(cmd=cmd).data[0][0]
                    cmd = f"SELECT count(id) FROM back_order WHERE execute_id={execute_id} and status='close' and step={i}"
                    trade_close = self.management_sql.db.items(cmd=cmd).data[0][0]
                    #--------------Trade: sell/buy
                    cmd = f"SELECT count(id) FROM back_order WHERE execute_id={execute_id} and action='buy' and step={i}"
                    trade_buy = self.management_sql.db.items(cmd=cmd).data[0][0]
                    cmd = f"SELECT count(id) FROM back_order WHERE execute_id={execute_id} and action='sell' and step={i}"
                    trade_sell = self.management_sql.db.items(cmd=cmd).data[0][0]
                    #--------------Detaile
                    cmd = f"SELECT min(profit_close), max(profit_close), max(profit_open), min(profit_open) FROM back_execute_detaile WHERE execute_id={execute_id} and step={i}"
                    data = self.management_sql.db.items(cmd=cmd).data[0]
                    profit_close_min = data[0]
                    profit_close_max = data[1]
                    profit_open_min = data[2]
                    profit_open_max=data[3]
                    #--------------Param
                    cmd = f"SELECT param FROM back_execute_detaile WHERE execute_id={execute_id} and step={i} and param !=''"
                    param = self.management_sql.db.items(cmd=cmd).data
                    param = param[0] if len(param)> 0 else ""
                    #--------------Add
                    detaile.append({
                        "step":f'{i}',
                        "date_from":date_from,
                        "date_to":date_to,
                        "trade_all":f"{trade_all}",
                        "trade_open":f"{trade_open}",
                        "trade_close":f"{trade_close}",
                        "trade_buy":f"{trade_buy}",
                        "trade_sell":f"{trade_sell}",
                        "profit_all":f"{profit_all:.{2}f}",
                        "profit_positive":f"{profit_positive:.{2}f}",
                        "profit_negative":f"{profit_negative:.{2}f}",
                        "profit_close_min":f"{profit_close_min:.{2}f}",
                        "profit_close_max":f"{profit_close_max:.{2}f}",
                        "profit_open_min":f"{profit_open_min:.{2}f}",
                        "profit_open_max":f"{profit_open_max:.{2}f}",
                        "param":param
                    })
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = detaile
            output.message=execute_id
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
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
        cmd = f"SELECT strategy.name, strategy_item.symbols, strategy_item.actions, strategy_item.amount, strategy_item.tp_pips, strategy_item.sl_pips, strategy_item.params, {table}.date_from, {table}.date_to, {table}.account_id, {table}.step, {table}.status, {table}.profit_manager_id, {table}.money_management_id FROM strategy JOIN strategy_item ON strategy.id = strategy_item.strategy_id JOIN {table} ON strategy_item.id = {table}.strategy_item_id WHERE {table}.id = {id}"
        result:model_output = self.management_sql.db.items(cmd=cmd)
        #--------------Data
        if result.status and len(result.data) > 0 :
            data = result.data[0]
            output["strategy_name"] = data[0]
            output["symbols"] = data[1]
            output["actions"] = data[2]
            output["amount"] = data[3]
            output["tp_pips"] = data[4]
            output["sl_pips"] = data[5]
            output["params"] = ast.literal_eval(data[6]) if data[6] else {}
            output["date_from"] = data[7]
            output["date_to"] = data[8]
            output["account_id"] = data[9]
            output["step"] = data[10]
            output["status"] = data[11]
            output["profit_manager_id"] = data[12]
            output["money_management_id"] = data[13]
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

    #--------------------------------------------- get_strategy_instance
    def get_strategy_instance(self, name, execute_detaile)-> model_output:
        #-------------- Variable
        output = model_output()
        #-------------- Action
        strategy_class = globals().get(name)
        if strategy_class and callable(strategy_class):
            output.data = strategy_class(params=execute_detaile)
        else:
            output.status = False
        #--------------Return
        return output