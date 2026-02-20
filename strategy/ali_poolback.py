#--------------------------------------------------------------------------------- Location
# strategy/dowjones.py

#--------------------------------------------------------------------------------- Description
# dowjones

#--------------------------------------------------------------------------------- Import
import inspect, time
from datetime import datetime, timedelta

from sqlalchemy import table, true
from logic.startup import debug, log_instance, list_instrument, Strategy_Run, Strategy_Action, Strategy_Run, database_management, database_data
from logic.util import model_output, sort, cal_size, get_tbl_name, cal_movement
from logic.log import Logic_Log
from logic.data_sql import Data_SQL
from logic.data_orm import Data_Orm

#--------------------------------------------------------------------------------- Class
class Ali_PoolBack:
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
        self.time_frame = params["params"]["time_frame"]
        self.region = params["params"]["region"]
        self.time_from = params["params"]["time_from"]
        self.time_to = params["params"]["time_to"]
        self.max_order = params["params"]["max_order"]
        self.domain = params["params"]["domain"]
        self.period = params["params"]["period"]
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
        switch_up = False
        switch_down = False
        tk_up = False
        tk_down = False
        kumo_up = False
        kumo_down = False
        #--------------Method
        #---inner_down
        def inner_down(count):
            count = count -1
            while count > 0:
                sa1 = average[count]['sa1']
                sb1 = average[count]['sb1']['average']
                if sa1 < sb1 : return False
                if sa1 > sb1 : return True
                if sa1 == sb1 : 
                    count = count -1
                    inner_down(count)
            return False
        #---inner_up
        def inner_up(count):
            count = count -1
            while count > 0:
                sa1 = average[count]['sa1']
                sb1 = average[count]['sb1']['average']
                if sa1 > sb1 : return False
                if sa1 < sb1 : return True
                if sa1 == sb1 : 
                    count = count -1
                    inner_up(count)
            return False
        #--------------Action
        try:
            #------average
            average = {}
            average_date = date
            for i in range(10, 0, -1):
                average_item = {}
                #---average
                for key, value in self.period.items():
                    high, low = self.box(date=average_date, count=value, time_frame=self.time_frame)
                    average_item[key] = {"high": high, "low": low , "average": (high+low)/2}
                #---sa
                average_item['sa1'] = (average_item['t1']['average'] + average_item['k1']['average']) / 2
                average_item['sa2'] = (average_item['t2']['average'] + average_item['k2']['average']) / 2
                average[i] = average_item
                average_date = average_date - timedelta(minutes=1)
            #------data
            sa_1 = average[self.domain]['sa1']
            sb_1 = average[self.domain]['sb1']['average']
            t2 =average[self.domain]['t2']['average']
            k2 = average[self.domain]['k2']['average']
            sa2 =average[self.domain]['sa2']
            sb2 = average[self.domain]['sb2']['average']
            #---------tk
            if t2 > k2 :
                tk_up = True
                tk_down = False
            else:
                tk_up = False
                tk_down = True
            #---------kumo
            if sa2 > sb2 :
                kumo_up = True
                kumo_down = False
            else:
                kumo_up = False
                kumo_down = True
            #---------switch_down
            if ask < sa_1 and ask < sb_1 and sa_1 < sb_1:
                switch_down = inner_down(count=self.domain)
            #---------switch_up
            if ask > sa_1 and ask > sb_1 and sa_1 > sb_1:
                switch_up = inner_up(count=self.domain)
            #---------Inter buy
            if tk_up and kumo_up and switch_down :
                #---price, amount 
                action = "buy"
                price, amount = cal_size(balance=self.balance, action=action, ask=self.ask, bid=self.bid, price=price, pips=self.sl_pips, risk=self.risk, digits=self.digits, point_size=self.point_size)
                #---sl
                self.sl_pips  = cal_movement(price, average[self.domain]['sb1']['low'], self.digits)
                #---tp
                self.tp_pips = self.sl_pips
                #---Item
                item = {
                    #---General
                    "state": Strategy_Action.PRICE_CHANGE,
                    "run": Strategy_Run.ORDER_OPEN,
                    "father_id": father_id,
                    "step": step,
                    "execute_id": self.execute_id,
                    "tp_pips": self.tp_pips, 
                    "sl_pips": self.sl_pips,
                    "digits": self.digits, 
                    "point_size": self.point_size,
                    #---Data
                    "symbol": symbol, 
                    "action": "buy", 
                    "amount": amount, 
                    "date": date,
                    "ask": price,
                    "bid": price,
                }
                items.append(item)
            #---------Inter sell
            if tk_down and kumo_down and switch_up :
                #---Amount
                action = "sell"
                price, amount = cal_size(balance=self.balance, action=action, ask=self.ask, bid=self.bid, price=price, pips=self.sl_pips, risk=self.risk, digits=self.digits, point_size=self.point_size)
                #---sl
                self.sl_pips  = cal_movement(price, average[self.domain]['sb1']['high'], self.digits)
                #---tp
                self.tp_pips = self.sl_pips
                #---Item
                item = {
                    #---General
                    "state": Strategy_Action.PRICE_CHANGE,
                    "run": Strategy_Run.ORDER_OPEN,
                    "father_id": father_id,
                    "step": step,
                    "execute_id": self.execute_id,
                    "tp_pips": self.tp_pips, 
                    "sl_pips": self.sl_pips,
                    "digits": self.digits, 
                    "point_size": self.point_size,
                    #---Data
                    "symbol": symbol, 
                    "action": "buy", 
                    "amount": amount, 
                    "date": date,
                    "ask": price,
                    "bid": price,
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
            table = get_tbl_name(self.symbol, self.time_frame)
            cmd = f"SELECT id, date, askclose, bidclose FROM {table} WHERE date>='{self.date_from}' and date<='{self.date_to}' ORDER BY date ASC"
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
    
    #---------------------------------------------box
    def box(
            self,
            date:int, 
            count:int,
            time_frame:str,
        ):
        #--------------Description
        # IN     : date | count | time_frame
        # OUT    : high | low
        # Action : این متد یک دیت می‌گیرد یک عدد می‌گیرد و یک تایم فریم می‌گیرد و های و لو آن بازه را برای ما برمی‌گرداند
        #--------------Action
        table = get_tbl_name(self.symbol, self.time_frame)
        date_to = date
        date_from = date - timedelta(minutes=count)
        cmd = f"SELECT MAX(askhigh), MIN(asklow) FROM {table} WHERE date>='{date_from}' and date<='{date_to}'"
        result = self.data_sql.db.items(cmd=cmd).data
        high = result[0][0]
        low = result[0][1]
        return high, low
    