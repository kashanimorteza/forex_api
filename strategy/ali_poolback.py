#--------------------------------------------------------------------------------- Location
# strategy/dowjones.py

#--------------------------------------------------------------------------------- Description
# dowjones

#--------------------------------------------------------------------------------- Import
import inspect, time
from datetime import datetime
from logic.startup import debug, log_instance, list_instrument, Strategy_Run, Strategy_Action, Strategy_Run, database_management, database_data
from logic.util import model_output, sort, time_change_newyork_utc, time_change_utc_newyork, cal_price_pips, cal_size, get_tbl_name
from logic.log import Logic_Log
from logic.data_sql import Data_SQL
from logic.data_orm import Data_Orm

#--------------------------------------------------------------------------------- Class
class Dowjones:
    #---------------------------------------------init
    def __init__(
            self, 
            params:dict=None, 
            log:Logic_Log=None
        ):
        #--------------debug
        self.this_class = self.__class__.__name__
        #--------------variable
        self.params = params
        self.log = log if log else log_instance
        #--------------strategy | items
        self.symbol = params["symbol"]
        self.actions = params["actions"].split(',')
        self.amount = params["amount"]
        self.tp_pips = params["tp_pips"]
        self.sl_pips = params["sl_pips"]
        self.trade_limit_profit= params["trade_limit_profit"]
        #--------------strategy | params
        self.time_start = datetime.strptime(params["params"]["time_start"], "%H:%M:%S").time()
        self.time_end = datetime.strptime(params["params"]["time_end"], "%H:%M:%S").time()
        self.change_pip = params["params"]["change_pip"]
        self.order_pip = params["params"]["order_pip"]
        self.down = params["params"]["down"]
        self.up = params["params"]["up"]
        self.pending_limit = params["params"]["pending_limit"]
        #--------------execute | items
        self.execute_id = params["execute_id"]
        self.date_from = params["date_from"]
        self.date_to = params["date_to"]
        self.money_management_id = params["money_management_id"]
        self.profit_manager_id = params["profit_manager_id"]
        #--------------general
        self.digits = list_instrument[self.symbol]["digits"]
        self.point_size = list_instrument[self.symbol]["point_size"]
        #--------------database
        self.management_sql = None
        self.management_orm = None
        self.data_sql = None
        #--------------data
        self.balance = None
        self.equity = None
        self.risk = None
        self.set_price = None
        self.set_order = None
        self.date:datetime = None
        self.ask = None
        self.bid = None
        self.price = None
    
    #---------------------------------------------start
    def start(
            self,
            father_id:int, 
            step:int,
        ):
        #--------------Description
        # IN     : 
        # OUT    : 
        # Action : Just buy|sell order
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
            # item = {
            #     #---General
            #     "state": Strategy_Action.START,
            #     "run": Strategy_Run.ORDER_OPEN,
            #     "father_id": father_id,
            #     "step": step,
            # }
            pass
        except Exception as e:  
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Output
        output.time = sort(f"{(time.time() - start_time):.3f}", 3)
        output.data = items
        output.message = f"exi({self.execute_id}) | sym({self.symbol}) | stp({step})"
        #--------------Verbose
        if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
        #--------------Log
        if log : self.log.log(log_model, output)
        #--------------Return
        return output

    #---------------------------------------------stop
    def stop(
            self,
            father_id:int, 
            step:int,
        ):
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
        #-------------- Output
        output = model_output()
        output.class_name = self.this_class
        output.method_name = this_method
        #--------------Variable
        items = []
        #--------------Action
        try:
            item = {
                #---General
                "state": Strategy_Action.ORDER_CLOSE,
                "run": Strategy_Run.ORDER_CLOSE_ALL,
                "father_id": father_id,
                "step": step,
            }
            items.append(item)
        except Exception as e:  
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Output
        output.time = sort(f"{(time.time() - start_time):.3f}", 3)
        output.data = items
        output.message = f"exi({self.execute_id}) | sym({self.symbol}) | stp({step})"
        #--------------Verbose
        if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
        #--------------Log
        if log : self.log.log(log_model, output)
        #--------------Return
        return output
    
    #---------------------------------------------order_action
    def order_action(
            self,
            father_id:int, 
            step:int,
            list_order_pending,
            list_order_open,
            list_order_close
        ):
        #-------------- Description
        # IN     : 
        # OUT    : 
        # Action : Just buy|sell order
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
        #--------------Action
        try:
            # item = {
            #     #---General
            #     "state": Strategy_Action.START,
            #     "run": Strategy_Run.ORDER_OPEN,
            #     "father_id": father_id,
            #     "step": step,
            # }
            pass
        except Exception as e:  
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Output
        output.time = sort(f"{(time.time() - start_time):.3f}", 3)
        output.data = items
        output.message = f"exi({self.execute_id}) | sym({self.symbol}) | stp({step})"
        #--------------Verbose
        if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
        #--------------Log
        if log : self.log.log(log_model, output)
        #--------------Return
        return output

    #---------------------------------------------price_change
    def price_change(
            self,
            father_id:int, 
            step:int,
            list_order_pending: list,
            list_order_open:list,
            list_order_close:list,
            symbol:str,
            date:datetime,
            ask:float,
            bid:float
        ):
        #-------------- Description
        # IN     : father_id, step, symbol, date, ask, bid
        # OUT    : items
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
        #--------------Action
        try:
            #---------Everyday
            if (self.set_order is None) or (self.set_order is False) or (date.date()> self.date.date()):
                #---------Time
                ny_date = time_change_utc_newyork(date)
                if self.time_start <= ny_date.time() <= self.time_end:
                    #---Set_Price
                    if not self.set_price or date.date()> self.date.date():
                        self.set_order = False
                        self.set_price = True
                        self.ask = ask
                        self.bid = bid
                        self.date = date
                    #---Check_Price
                    if self.set_price: 
                        movement = abs(ask - self.ask)
                        if movement >= self.change_pip:
                            self.set_order = True
                            self.set_price = False
                            action = self.up if ask > self.ask else self.down
                            if action == "buy":
                                price = cal_price_pips(self.ask, -self.order_pip , self.digits, self.point_size)
                            else:
                                price = cal_price_pips(self.bid, self.order_pip , self.digits, self.point_size)
                            if self.risk > 0 :
                                amount = cal_size(balance=self.balance, price=price, pips=self.sl_pips, risk=self.risk, digits=self.digits, point_size=self.point_size)
                            else:
                                amount = self.amount
                            amount = float(f"{amount:.{2}f}")
                            item = {
                                #---General
                                "state": Strategy_Action.PRICE_CHANGE,
                                "run": Strategy_Run.ORDER_PENDING,
                                "father_id": father_id,
                                "step": step,
                                "execute_id": self.execute_id,
                                "tp_pips": self.tp_pips, 
                                "sl_pips": self.sl_pips,
                                "digits": self.digits, 
                                "point_size": self.point_size,
                                #---Data
                                "symbol": symbol, 
                                "action": action, 
                                "amount": amount, 
                                "date": date,
                                "ask": price,
                                "bid": price,
                                "pending_limit": self.pending_limit,
                            }
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

    #---------------------------------------------back
    def back(self):
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
        result = model_output()
        #--------------Action
        try:
            #------Database
            self.database(action="open")
            #------money_management
            cmd = f"SELECT balance, risk, limit_profit, limit_loss, limit_trade, limit_stop FROM money_management WHERE id={self.money_management_id}"
            self.money_management = self.management_sql.db.items(cmd=cmd).data[0]
            self.balance = self.money_management[0]
            self.equity = self.money_management[0]
            self.risk = self.money_management[1]
            #------Step
            step = self.management_sql.db.item(cmd=f"SELECT MAX(step) FROM back_order WHERE execute_id={self.execute_id}").data
            step = (step + 1) if step else 1
            #------Logic_Back
            from logic.back import Logic_Back
            logic_back = Logic_Back(
                management_sql=self.management_sql, 
                data_sql=self.data_sql, 
                management_orm=self.management_orm
            )
            logic_back.load(params=self.params)
            logic_back.step= step
            #------Verbose
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.message = f"exi({self.execute_id}) | sym({self.symbol}) | stp({step})"
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
            #------Data
            table = get_tbl_name(self.symbol, "t1")
            cmd = f"SELECT id, date, ask, bid FROM {table} WHERE date>='{self.date_from}' and date<='{self.date_to}' ORDER BY date ASC"
            data = self.data_sql.db.items(cmd=cmd).data
            #------Start
            result= self.start(father_id=-1, step=step)
            if result.data : logic_back.action(items=result.data)
            self.management_sql.db.execute(cmd=f"UPDATE back_execute SET status='{Strategy_Action.START}' WHERE id={self.execute_id}")
            #------Next
            for row in data:
                #------price_data
                logic_back.date = row[1]
                logic_back.ask = float(row[2])
                logic_back.bid = float(row[3])
                #------check_pending_order
                if len(logic_back.list_order_pending)>0 : 
                    logic_back.check_pending_order()
                #------check_profit_manager
                if len(logic_back.list_order_open)>0 : 
                    logic_back.check_profit_manager()
                #------check_tp_sl
                if len(logic_back.list_order_open)>0 : 
                    logic_back.check_tp_sl()
                #------check_limit
                if len(logic_back.list_order_open)>0 : 
                    logic_back.check_limit()
                #------balance_update
                self.balance = logic_back.balance
                self.equity = logic_back.equity
                #------strategy | order_action
                if logic_back.order_open_accept and (logic_back.order_action_open or logic_back.order_action_close):
                    result = self.order_action(
                        father_id=-1,
                        step=step,
                        list_order_pending = logic_back.list_order_pending,
                        list_order_open= logic_back.list_order_open,
                        list_order_close = logic_back.list_order_close
                    )
                    if logic_back.order_action_open : logic_back.order_action_open = False
                    if logic_back.order_action_close : logic_back.order_action_close = False
                    if result.data : logic_back.action(items=result.data)
                #------strategy | price_change
                if logic_back.order_open_accept:
                    result = self.price_change(
                        father_id=-1,
                        step=step,
                        list_order_pending = logic_back.list_order_pending,
                        list_order_open= logic_back.list_order_open,
                        list_order_close = logic_back.list_order_close,
                        symbol=self.symbol,
                        date=logic_back.date,
                        ask=logic_back.ask,
                        bid=logic_back.bid
                    )
                    if result.data : 
                        logic_back.action(items=result.data)
                #------order_open_accept
                if not logic_back.order_open_accept : 
                    break
            #--------------Stop
            result = self.stop(father_id=-1, step=step)
            if result.data : logic_back.action(items=result.data)
            self.management_sql.db.execute(cmd=f"UPDATE back_execute SET status='{Strategy_Action.STOP}' WHERE id={self.execute_id}")
            #--------------Database
            self.database(action="close")
        except Exception as e:  
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Output
        output.time = sort(f"{(time.time() - start_time):.3f}", 3)
        output.data = None
        output.message = f"{self.execute_id} | {self.this_class} | {self.symbol}"
        #--------------Verbose
        if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
        #--------------Log
        if log : self.log.log(log_model, output)
        #--------------Return
        return output

    #---------------------------------------------database
    def database(self, action):
        #--------------Description
        # IN     : 
        # OUT    : 
        # Action : Just buy|sell order
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
            if action=="open":
                if self.management_orm == None:
                    self.management_orm = Data_Orm(database=database_management)
                if self.management_sql ==None:
                    self.management_sql = Data_SQL(database=database_management)
                    self.management_sql.db.open()
                if self.data_sql==None:
                    self.data_sql = Data_SQL(database=database_data)
                    self.data_sql.db.open()
            if action=="close":
                self.management_sql.db.close()
                self.data_sql.db.close()
        except Exception as e:  
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Output
        output.time = sort(f"{(time.time() - start_time):.3f}", 3)
        output.data = None
        output.message = None
        #--------------Verbose
        if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
        #--------------Log
        if log : self.log.log(log_model, output)
        #--------------Return
        return output
    
#---------------------------------------------Comment
#time_from_ny_to_utc = time_change_newyork_utc(datetime.combine(self.date_from.date(), self.time_start))
#time_from_ny_to_utc = time_from_ny_to_utc - timedelta(hours=1)
#time_to_ny_to_utc = time_change_newyork_utc(datetime.combine(self.date_from.date(), self.time_end))
#time_to_ny_to_utc = time_to_ny_to_utc + timedelta(hours=1)
#cmd = f"SELECT id, date, ask, bid FROM {table} WHERE date>='{self.date_from}' and date<='{self.date_to}' AND date::time BETWEEN '{time_from_ny_to_utc.time()}' AND '{time_to_ny_to_utc.time()}' ORDER BY date ASC"
#cmd = f"SELECT id, date, ask, bid FROM {table} WHERE date>='{self.date_from}' and date<='{self.date_to}' and (date AT TIME ZONE 'UTC' AT TIME ZONE 'America/New_York')::time BETWEEN '{self.time_start}' AND '{self.time_end}' ORDER BY date ASC"