#--------------------------------------------------------------------------------- Location
# logic/logic_back.py

#--------------------------------------------------------------------------------- Description
# logic_back

#--------------------------------------------------------------------------------- Import
from operator import eq
import inspect, time, ast
from logic.startup import Strategy_Action, Strategy_Run, debug, list_instrument, log_instance, database_management, database_data
from logic.util import model_output, sort, get_tbl_name, time_change_utc_newyork, cal_price, cal_tp_sl, cal_movement, cal_percent_of_value, cal_value_of_percent, cal_profit
from logic.startup import data_instance
from logic.log import Logic_Log
from logic.data_sql import Data_SQL
from logic.data_orm import Data_Orm
from model.back_order import model_back_order_db
from strategy import *
from model import *

#--------------------------------------------------------------------------------- Class
class Logic_Back:
    #---------------------------------------------init
    def __init__(
            self,
            management_sql:Data_SQL=None, 
            management_orm:Data_Orm=None, 
            data_sql:Data_SQL=None, 
            log:Logic_Log=None
        ):
        #--------------debug
        self.this_class = self.__class__.__name__
        #--------------database
        self.management_orm = management_orm if management_orm else data_instance["management_orm"]
        self.management_sql = management_sql if management_sql else data_instance["management_sql"]
        self.data_sql = data_sql if data_sql else data_instance["data_sql"]
        #--------------log
        self.log = log if log else log_instance
        #--------------Variable
        self.list_order_pending:list[dict] = []
        self.list_order_open:list[tuple] = []
        self.list_order_close:list[tuple] = []

        self.balance_base = None
        self.balance = None
        self.equity_base = None
        self.equity = None

        self.step = None
        self.date = None
        self.ask = None
        self.bid = None

        self.order_open_accept = True
        self.order_action_open = False
        self.order_action_close = False

        self.account_profit_open = 0
        self.account_profit_close = 0
        self.account_profit_profit = 0

    #---------------------------------------------load
    def load(self, params):
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
            self.execute_id = params["execute_id"]
            self.money_management_id = params["money_management_id"]
            self.profit_manager_id = params["profit_manager_id"]
            self.symbol = params["symbol"]
            self.actions = params["actions"].split(',')
            self.amount = params["amount"]
            self.tp_pips = params["tp_pips"]
            self.sl_pips = params["sl_pips"]
            self.date_from = params["date_from"]
            self.date_to = params["date_to"]
            self.trade_limit_profit= params["trade_limit_profit"]
            self.digits = list_instrument[self.symbol]["digits"]
            self.point_size = list_instrument[self.symbol]["point_size"]
            #--------------Data
            cmd = f"SELECT * FROM profit_manager_item WHERE profit_manager_id={self.profit_manager_id} ORDER BY value DESC"
            self.profit_manager_items = self.management_sql .db.items(cmd=cmd).data 
            cmd = f"SELECT balance, risk, limit_profit, limit_loss, limit_trade, limit_stop FROM money_management WHERE id={self.money_management_id}"
            self.money_management = self.management_sql .db.items(cmd=cmd).data[0]
            #--------------money_management
            self.balance_base = self.money_management[0]
            self.balance = self.money_management[0]
            self.equity_base = self.money_management[0]
            self.equity = self.money_management[0]
            self.risk = self.money_management[1]
            self.account_limit_profit = self.money_management[2]
            self.account_limit_loss = self.money_management[3]
            self.account_limit_trade = self.money_management[4]
            self.account_limit_stop = self.money_management[5]
        except Exception as e:  
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #------Output
        output.time = sort(f"{(time.time() - start_time):.3f}", 3)
        output.data = params
        output.message = None
        #------Verbose
        if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
        #------Log
        if log : self.log.log(log_model, output)
        #--------------Return
        return output
    
    #---------------------------------------------run
    def run(self, execute_id):
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
            execute_detaile:model_output = self.execute_detaile(id=execute_id)
            strategy_name = execute_detaile["strategy_name"]
            strategy = self.get_strategy_instance(strategy_name, execute_detaile).data
            output = strategy.back()
        except Exception as e:  
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #------Output
        output.time = sort(f"{(time.time() - start_time):.3f}", 3)
        #------Verbose
        if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
        #------Log
        if log : self.log.log(log_model, output)
        #--------------Return
        return output
    
    #---------------------------------------------check_pending_order
    def check_pending_order(self)-> model_output:
        #--------------Description
        # IN     : 
        # OUT    : 
        # Action :
        #--------------Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        start_time = time.time()
        #--------------Output
        output = model_output()
        output.class_name = self.this_class
        output.method_name = this_method
        #--------------Action
        try:
            for order in self.list_order_pending:
                if (self.date - order["date"]).seconds <= order["pending_limit"]:
                    if order["action"]=="buy":
                        if self.ask >= order["ask"]:
                            #---update
                            order.update({"date": self.date, "ask": self.ask, "bid": self.bid})
                            #---verbose
                            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
                            output.message = f"{self.date} | {self.symbol} | {sort(order['action'], 4)} | amt({order['amount']}) | prc({order['ask']}) | ask({self.ask}) | Active"
                            self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
                            #---action
                            self.order_open(order)
                            self.list_order_pending.remove(order)
                            output.data = order
                    if order["action"] =="sell":
                        if self.bid <= order["bid"]:
                            #---update
                            order.update({"date": self.date, "ask": self.ask, "bid": self.bid})
                            #---verbose
                            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
                            output.message = f"{self.date} | {self.symbol} | {sort(order['action'], 4)} | amt({order['amount']}) | prc({order['bid']}) | bid({self.bid}) | Active"
                            self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
                            #---action
                            self.order_open(order)
                            self.list_order_pending.remove(order)
                            output.data = order
                else:
                    #---verbose
                    output.time = sort(f"{(time.time() - start_time):.3f}", 3)
                    output.message = f"{self.date} | {self.symbol} | {sort(order['action'], 4)} | amt({order['amount']}) | prc({order['ask']}) | Remove"
                    self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
                    #---action
                    self.list_order_pending.remove(order)
                    output.data = order
        except Exception as e:  
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Output
        output.time = sort(f"{(time.time() - start_time):.3f}", 3)
        #--------------Verbose
        if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
        #--------------Log
        if log : self.log.log(log_model, output)
        #--------------Return
        return output

    #---------------------------------------------check_profit_manager
    def check_profit_manager(self)-> model_output:
        #--------------Description
        # IN     : 
        # OUT    : 
        # Action :
        #--------------Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        start_time = time.time()
        #--------------Output
        output = model_output()
        output.class_name = self.this_class
        output.method_name = this_method
        #--------------Variable
        items = []
        #--------------Action
        try:
            for order in self.list_order_open:
                execute = False
                #---Order
                execute_id = order[1]
                step = order[2]
                order_id = order[0]
                order_price_open = order[5]
                order_action = order[11]
                order_price_tp = order[13]
                order_price_sl = order[14]
                order_pm = order[16]
                #---Movement
                movement = cal_movement(order_action, order_price_open, self.ask, self.bid, self.digits)
                #---PM
                if movement>0:
                    for pm in self.profit_manager_items:
                        if pm[2] == order_pm : break # agar profit_manager_item اجرا شده باشد دیگر بررسی نکند
                        value = pm[3]
                        tp_value = pm[4]
                        sl_value = pm[5]
                        percent = cal_percent_of_value(self.tp_pips, movement)
                        if percent >= value:
                            if tp_value and abs(tp_value)>0:
                                pips = cal_value_of_percent(self.tp_pips, abs(tp_value), self.digits, self.point_size)
                                if tp_value>0:
                                    if order_action == "buy":
                                        tp = cal_price(order_price_tp, pips, self.digits, self.point_size)
                                    else:
                                        tp = cal_price(order_price_tp, -pips, self.digits, self.point_size)
                                else:
                                    if order_action == "buy":
                                        tp = cal_price(order_price_tp, -pips, self.digits, self.point_size)
                                    else:
                                        tp = cal_price(order_price_tp, +pips, self.digits, self.point_size)
                                cmd = f"UPDATE back_order SET tp={tp}, profit_manager='{pm[2]}' WHERE id={order_id}"
                                self.management_sql.db.execute(cmd=cmd)
                                cmd = f"INSERT INTO back_profit_manager_detaile (date, order_id, ask, bid, execute, value) VALUES('{self.date}', {order_id}, {self.ask}, {self.bid}, 'TP', {tp})"
                                self.management_sql.db.execute(cmd=cmd)
                                #---update list
                                self.list_order_open = self.management_sql.db.items(cmd=f"select * FROM back_order WHERE execute_id='{execute_id}' and step='{step}' AND status='open'").data
                                #---verbose
                                message = f"{self.date} | {self.symbol} | {sort(order_action, 4)} | {order_id} | {pm[2]} | TP | old({order_price_tp}) | {pips} | new({tp})"
                                output.time = sort(f"{(time.time() - start_time):.3f}", 3)
                                self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", message)
                                items.append(order)
                                execute = True
                            if sl_value and abs(sl_value)>0:
                                pips = cal_value_of_percent(self.sl_pips, abs(sl_value), self.digits, self.point_size)
                                if sl_value>0:
                                    if order_action == "buy":
                                        sl = cal_price(order_price_sl, -pips, self.digits, self.point_size)
                                    else:
                                        sl = cal_price(order_price_sl, pips, self.digits, self.point_size)
                                else:
                                    if order_action == "buy":
                                        sl = cal_price(order_price_sl, pips, self.digits, self.point_size)
                                    else:
                                        sl = cal_price(order_price_sl, -pips, self.digits, self.point_size)
                                cmd = f"UPDATE back_order SET sl={sl}, profit_manager='{pm[2]}' WHERE id={order_id}"
                                self.management_sql.db.execute(cmd=cmd)
                                cmd = f"INSERT INTO back_profit_manager_detaile (date, order_id, ask, bid, execute, value) VALUES('{self.date}', {order_id}, {self.ask}, {self.bid}, 'SL', {sl})"
                                self.management_sql.db.execute(cmd=cmd)
                                #---update list
                                self.list_order_open = self.management_sql.db.items(cmd=f"select * FROM back_order WHERE execute_id='{execute_id}' and step='{step}' AND status='open'").data
                                #---verbose
                                message = f"{self.date} | {self.symbol} | {sort(order_action, 4)} | {order_id} | {pm[2]} | SL | old({order_price_sl}) | {pips} | new({sl})"
                                output.time = sort(f"{(time.time() - start_time):.3f}", 3)
                                self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", message)
                                items.append(order)
                                execute = True
                            if execute : break
        except Exception as e:  
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Output
        output.time = sort(f"{(time.time() - start_time):.3f}", 3)
        output.data = items
        output.message =  f"{self.date} | {len(output.data)}"
        #--------------Verbose
        if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
        #--------------Log
        if log : self.log.log(log_model, output)
        #--------------Return
        return output
    
    #---------------------------------------------check_limit
    def check_limit(self)-> model_output:
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
        #--------------Variable
        result = True
        param = ''
        profit_close = 0
        profit_open = 0
        trade_count = 0
        loss = 0
        #--------------action
        try:
            #--------------Order:Open
            for order in self.list_order_open :
                profit_trade = cal_profit(
                    action=order[11], 
                    amount=order[12], 
                    price_open=order[5], 
                    ask=self.ask, 
                    bid=self.bid, 
                    digits=self.digits, 
                    point_size=self.point_size
                )[0]
                if self.trade_limit_profit !=-1 and profit_trade >= self.trade_limit_profit:
                    order_dict = self.order_to_dict(order = order)
                    order_dict["date"] = self.date
                    order_dict["ask"] = self.ask
                    order_dict["bid"] = self.bid
                    self.order_close(item=order_dict).data["profit"]
                else:
                    trade_count += 1
                    profit_open = profit_open + profit_trade
            #--------------Order:Close
            for order in self.list_order_close : 
                trade_count += 1
                profit_close = profit_close + order[8]
            #--------------Check:Trade
            if self.account_limit_trade !=-1 and trade_count >= self.account_limit_trade : 
                result = False
                param = 'trade'
                self.order_open_accept = False
            #--------------Check:Stop
            if result and self.account_limit_stop !=-1 and profit_close >= self.account_limit_stop:
                result = False
                param='stop'
                self.order_open_accept = False
            #--------------Check:Profit
            profit = profit_open + profit_close
            if result and self.account_limit_profit !=-1 and profit >= self.account_limit_profit:
                result = False
                param='profit'
                self.order_open_accept = False
            #--------------Check:Loss
            loss = profit_open + profit_close
            if result and self.account_limit_loss !=-1 and loss<0 and loss <= self.account_limit_loss:
                result = False
                param='loss'
                self.order_open_accept = False
            #--------------Log
            if not result: param = f"{param} | {self.date}"
            if (self.account_profit_close != profit_close or self.account_profit_open != profit_open):
                if (abs(profit_close-self.account_profit_close)>1 or abs(profit_open-self.account_profit_open)>1) :
                    self.account_profit_close = profit_close
                    self.account_profit_open = profit_open
                    self.profit = profit_open + profit_close
                    cmd = f"INSERT INTO back_execute_detaile (date, execute_id, step, profit_close, profit_open, profit, param) VALUES('{self.date}', {self.execute_id}, {self.step}, {profit_close}, {profit_open},{(profit_open + profit_close)}, '{param}')"
                    self.management_sql.db.execute(cmd=cmd)
            #--------------output
            self.balance = float(f"{self.balance_base + profit_close:.{2}f}")
            self.equity = float(f"{self.equity_base + profit_open:.{2}f}")
            output.data = result, param
        except Exception as e:  
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Output
        output.time = sort(f"{(time.time() - start_time):.3f}", 3)
        output.message = f"{self.date} | {len(output.data)}"
        #--------------Verbose
        if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
        #--------------Log
        if log : self.log.log(log_model, output)
        #--------------Return
        return output
    
    #---------------------------------------------check_tp_sl
    def check_tp_sl(self)-> model_output:
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
        #--------------Variable
        items = []
        result = ''
        #--------------Action
        try:
            for order in self.list_order_open :
                #------Reset
                fire = False
                #------Data
                action = order[11]
                tp = order[13]
                sl = order[14]
                #------Check Buy
                if action == "buy":
                    if self.bid > tp and tp > 0 : 
                        fire = True
                        result = 'T'
                    if self.bid < sl and sl > 0 : 
                        fire = True
                        result = 'S'
                #------Check Sell
                if action == "sell":
                    if self.ask < tp and tp > 0 :
                        fire = True
                        result = 'T'
                    if self.ask > sl and sl > 0 : 
                        fire = True
                        result = 'S'
                #------Fire
                if fire :
                    item = self.order_to_dict(order)
                    item['date'] = self.date
                    item['ask'] = self.ask
                    item['bid'] = self.bid
                    item['result'] = result
                    item = self.order_close(item=item).data
                    items.append(item)
        except Exception as e:  
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Output
        output.time = sort(f"{(time.time() - start_time):.3f}", 3)
        output.data = items
        output.message = None
        #--------------Verbose
        if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
        #--------------Log
        if log : self.log.log(log_model, output)
        #--------------Return
        return output
    
    #---------------------------------------------action
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

    #---------------------------------------------order_pending
    def order_pending(self, item:dict)-> model_output:
        #--------------Description
        # IN     :
        # OUT    : 
        # Action :
        #--------------Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        start_time = time.time()
        #--------------Output
        output = model_output()
        output.class_name = self.this_class
        output.method_name = this_method
        #--------------Action
        try:
            self.list_order_pending.append(item)
        except Exception as e:  
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Output
        output.time = sort(f"{(time.time() - start_time):.3f}", 3)
        output.status = True
        output.data = self.list_order_pending
        output.message = f"{item['date']} | {item['symbol']} | {sort(item['action'], 4)} | amt({item['amount']}) | prc({item['ask']}) | lim({item['pending_limit']}) | Placed"
        #--------------Verbose
        if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
        #--------------Log
        if log : self.log.log(log_model, output)
        #--------------Return
        return output
    
    #---------------------------------------------order_open
    def order_open(self, item:dict)-> model_output:
        #--------------Description
        # IN     :
        # OUT    : 
        # Action :
        #--------------Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        start_time = time.time()
        #--------------Output
        output = model_output()
        output.class_name = self.this_class
        output.method_name = this_method
        #--------------Action
        try:
            #------Data
            father_id = item.get("father_id")
            execute_id = item.get("execute_id")
            step = item.get("step")
            digits = item.get("digits")
            point_size = item.get("point_size")
            symbol = item.get("symbol")
            action = item.get("action")
            amount = item.get("amount")
            tp_pips = item.get("tp_pips")
            sl_pips = item.get("sl_pips")
            ask = item.get("ask")
            bid = item.get("bid")
            date = item.get("date")
            #------TP/SL
            price_open, tp, sl, spread = cal_tp_sl(action, ask, bid, tp_pips, sl_pips, digits, point_size)
            #------Action
            obj = model_back_order_db()
            obj.father_id = father_id
            obj.execute_id = execute_id
            obj.step = step
            obj.symbol = symbol
            obj.action = action
            obj.amount = amount
            obj.date_open = date
            obj.price_open = price_open
            obj.tp = tp
            obj.sl = sl
            obj.spread = spread
            obj.profit_manager = ''
            obj.ask = ask
            obj.bid = bid
            obj.status = 'open'
            obj.balance = self.balance
            obj.equity = self.equity
            #------ Database
            result_database:model_output = self.management_orm.add(model=model_back_order_db, item=obj)
            #------Update
            self.list_order_open = self.management_sql.db.items(cmd=f"select * FROM back_order WHERE execute_id='{execute_id}' and step='{step}' AND status='open'").data
            self.order_action_open = True
        except Exception as e:  
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #------Output
        output.time = sort(f"{(time.time() - start_time):.3f}", 3)
        output.status = result_database.status
        output.data = item
        output.message = f"{date} | {symbol} | {sort(action, 4)} | amt({amount}) | prc({price_open}) | tpt({tp}) | sls({sl})"
        #--------------Verbose
        if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
        #--------------Log
        if log : self.log.log(log_model, output)
        #--------------Return
        return output

    #---------------------------------------------order_close
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
            execute_id = item.get("execute_id")
            step = item.get("step")
            result = item.get("result")
            rr = ''
            #------ Profit
            profit, price_close = cal_profit(action, amount, price_open, ask, bid, digits, point_size)
            item["profit"] = profit
            item["price_close"] = price_close
            item["date_close"] = date
            item["status"] = 'close'

            if profit>0: 
                item["result"] = 'T'
                result = 'T'

            #------ risk-to-reward ratio (R/R)
            if profit>0:
                loss_price = cal_price(price_open, -self.sl_pips, self.digits, self.point_size)
                p_loss, _ = cal_profit(action, amount, price_open, loss_price, loss_price, digits, point_size)
                rr = abs(float(f"{profit/p_loss:.{2}f}"))
            #------ Database
            cmd = f"UPDATE back_order SET date_close='{date}', price_close={price_close}, profit={profit}, result='{result}', rr='{rr}', status='close' WHERE id='{id}'"
            result_database:model_output = self.management_sql.db.execute(cmd=cmd)
            #------Update
            self.list_order_open = self.management_sql.db.items(cmd=f"select * FROM back_order WHERE execute_id='{execute_id}' and step='{step}' AND status='open'").data
            self.list_order_close = self.management_sql.db.items(cmd=f"select * FROM back_order WHERE execute_id='{execute_id}' and step='{step}' AND status='close'").data
            self.order_action_close = True
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

    #---------------------------------------------order_close_all
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
        #-------------- Variable
        output.data = []
        #-------------- Action
        try:
            for order in self.list_order_open :
                #------Data
                item = self.order_to_dict(order)
                item.update({"date": self.date, "ask": self.ask, "bid": self.bid})
                result = self.order_close(item=item).data
                output.data.append(result)
                profit =  result["profit"]
                self.account_profit_close = self.account_profit_close + profit
                self.balance = self.balance + profit
            #self.strategy.balance = self.balance
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
    
    #---------------------------------------------get_data
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
                cmd = f"SELECT min(profit_close), max(profit_close), max(profit_open), min(profit_open), min(profit), max(profit) FROM back_execute_detaile WHERE execute_id={execute_id}"
                data = self.management_sql.db.items(cmd=cmd).data[0]
                profit_close_min = data[0]
                profit_close_max = data[1]
                profit_open_min = data[2]
                profit_open_max=data[3]
                profit_min = data[4]
                profit_max=data[5]
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
                    "profit_min":f"{profit_min:.{2}f}",
                    "profit_max":f"{profit_max:.{2}f}",
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
                    cmd = f"SELECT min(profit_close), max(profit_close), max(profit_open), min(profit_open), min(profit), max(profit) FROM back_execute_detaile WHERE execute_id={execute_id} and step={i}"
                    data = self.management_sql.db.items(cmd=cmd).data[0]
                    profit_close_min = data[0]
                    profit_close_max = data[1]
                    profit_open_min = data[2]
                    profit_open_max=data[3]
                    profit_min = data[4]
                    profit_max=data[5]
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
                        "profit_min":f"{profit_min:.{2}f}",
                        "profit_max":f"{profit_max:.{2}f}",
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
    def execute_detaile(self, id) -> dict:
        #-------------- Variable
        output = {}
        #--------------Data
        table = "back_execute"
        #--------------Action
        cmd = f"SELECT strategy.name, strategy_item.symbols, strategy_item.actions, strategy_item.amount, strategy_item.tp_pips, strategy_item.sl_pips,strategy_item.limit_profit, strategy_item.params, {table}.id, {table}.date_from, {table}.date_to, {table}.account_id, {table}.status, {table}.profit_manager_id, {table}.money_management_id FROM strategy JOIN strategy_item ON strategy.id = strategy_item.strategy_id JOIN {table} ON strategy_item.id = {table}.strategy_item_id WHERE {table}.id = {id}"
        result:model_output = self.management_sql.db.items(cmd=cmd)
        #--------------Data
        if result.status and len(result.data) > 0 :
            data = result.data[0]
            output["strategy_name"] = data[0]
            output["symbol"] = data[1]
            output["actions"] = data[2]
            output["amount"] = data[3]
            output["tp_pips"] = data[4]
            output["sl_pips"] = data[5]
            output["trade_limit_profit"] = data[6]
            output["params"] = ast.literal_eval(data[7]) if data[7] else {}
            output["execute_id"] = data[8]
            output["date_from"] = data[9]
            output["date_to"] = data[10]
            output["account_id"] = data[11]
            output["status"] = data[12]
            output["profit_manager_id"] = data[13]
            output["money_management_id"] = data[14]
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

    #---------------------------------------------get_strategy_instance
    def get_strategy_instance(self, name, params)-> model_output:
        #-------------- Variable
        output = model_output()
        #-------------- Action
        strategy_class = globals().get(name)
        if strategy_class and callable(strategy_class):
            output.data = strategy_class(params=params)
        else:
            output.status = False
        #--------------Return
        return output
    
    #---------------------------------------------order_to_dict
    def order_to_dict(self, order)-> dict:
        #-------------- Description
        # IN     :
        # OUT    : 
        # Action :
        #-------------- Output
        output:dict = {}
        #-------------- Action
        output["id"] = order[0]
        output["execute_id"] = order[1]
        output["step"] = order[2]
        output["father_id"] = order[3]
        output["date_open"] = order[4]
        output["price_open"] = order[5]
        output["date_close"] = order[6]
        output["price_close"] = order[7]
        output["profit"] = order[8]
        output["status"] = order[9]
        output["symbol"] = order[10]
        output["action"] = order[11]
        output["amount"] = order[12]
        output["tp"] = order[13]
        output["sl"] = order[14]
        output["spread"] = order[15]
        output["profit_manager"] = order[16]
        output["ask"] = order[17]
        output["bid"] = order[18]
        output["order_id"] = order[19]
        output["trade_id"] = order[20]
        output["description"] = order[21]
        output["enable"] = order[22]
        output["balance"] = order[23]
        output["equity"] = order[24]
        #--------------Return
        return output