#--------------------------------------------------------------------------------- Location
# myStrategy/st_01.py

#--------------------------------------------------------------------------------- Description
# st_01

#--------------------------------------------------------------------------------- Import
import inspect, time
from myLib.model import model_output
from myLib.logic_global import debug, log_instance, data_instance
from myLib.utils import sort
from myLib.log import Log
from myLib.data_orm import Data_Orm
from myLib.data_sql import Data_SQL
from myLib.forex import Forex
from myModel.model_live_order import model_live_order_db
from myModel.model_live_execute import model_live_execute_db

#--------------------------------------------------------------------------------- Action
class Floating:
    #--------------------------------------------- init
    def __init__(
            self,
            execute_id=None,
            params=None,
            forex:Forex=None,
            data_orm:Data_Orm=None, 
            data_sql:Data_SQL=None,
            log:Log=None
        ):
        #-------------- Variable
        self.this_class = self.__class__.__name__
        self.execute_id = execute_id
        self.params = params
        self.forex = forex
        #-------------- Instance
        self.log = log if log else log_instance
        self.data_orm = data_orm if data_orm else data_instance["management_orm"]
        self.data_sql = data_sql if data_sql else data_instance["management_sql"]
        self.data_sql_data = data_sql if data_sql else data_instance["data_sql"]
        
    #--------------------------------------------- start
    def start(self):
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
        
        try:
            #--------------Data
            actions = self.params["actions"].split(',')
            symbols = self.params["symbols"].split(',')
            amount = self.params["amount"]
            tp_pips = self.params["tp_pips"]
            sl_pips = self.params["st_pips"]
            #--------------Forex
            for symbol in symbols :
                for action in actions :
                    result:model_output = self.forex.order_open(
                        action=action, 
                        symbol=symbol,
                        amount=amount,
                        tp_pips=tp_pips,
                        sl_pips=sl_pips,
                        execute_id=self.execute_id
                    )
            #--------------Database
            if result.status:
                cmd = f"UPDATE live_execute SET status='{this_method}' WHERE id={self.execute_id}"
                self.data_sql.db.execute(cmd=cmd)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = self.execute_id
            output.message = self.execute_id
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
        #-------------- Variable
        order_ids = []

        try:
            #--------------Database
            cmd = f"UPDATE live_execute SET status='{this_method}' WHERE id='{self.execute_id}';"
            self.data_sql.db.execute(cmd=cmd)
            #--------------Action
            orders:model_output = self.data_orm.items(model=model_live_order_db, execute_id=self.execute_id, status='open')
            if orders.status:
                for order in orders.data : order_ids.append(order.order_id)
                if len(order_ids)>0 : self.forex.order_close(order_ids=order_ids)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = self.execute_id
            output.message = self.execute_id
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
    
    #--------------------------------------------- order_close
    def order_close(self, order_detaile):
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
        
        try:
            #--------------Data
            action = order_detaile["action"]
            symbol = order_detaile["symbol"]
            amount = order_detaile["amount"]
            tp_pips = self.params["tp_pips"]
            sl_pips = self.params["st_pips"]
            profit = order_detaile["profit"]
            trade_id = order_detaile["trade_id"]
            #--------------Check
            if profit < 0 :
                action = "sell" if action == "buy" else "buy"
            #--------------Forex
            result:model_output = self.forex.order_open(
                action=action, 
                symbol=symbol,
                amount=amount,
                tp_pips=tp_pips,
                sl_pips=sl_pips,
                execute_id=self.execute_id
            )
            #--------------Database
            if result.status:
                cmd = f"UPDATE live_execute SET status='{this_method}' WHERE id={self.execute_id};"
                self.data_sql.db.execute(cmd=cmd)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = self.execute_id
            output.message = f" {trade_id} | {order_detaile['action']}:{profit} | {action},{symbol},{amount},{tp_pips},{sl_pips},{result.status}"
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

    #--------------------------------------------- price_change
    def price_change(self, order_detail):
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
        execute_id = self.execute_id
        params = self.params
        order_detaile = order_detaile.data
        
        try:
            #--------------Data
            action = params["action"]
            symbol = params["symbol"]
            amount = params["amount"]
            tp_pips = params["tp_pips"]
            sl_pips = params["st_pips"]
            #--------------Check
            action = "sell" if order_detaile["action"] == "buy" else "buy"
            #--------------Forex
            result:model_output = self.forex.order_open(
                action=action, 
                symbol=symbol,
                amount=amount,
                tp_pips=tp_pips,
                sl_pips=sl_pips,
                execute_id=execute_id
            )
            #--------------Database
            if result.status:
                cmd = f"UPDATE live_execute SET status='{this_method}' WHERE id={execute_id};"
                database:model_output = self.data_sql.db.execute(cmd=cmd)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = execute_id
            output.message = f"{execute_id} | {result.status} | {database.status} | {action} | {symbol} | {amount} | {tp_pips} | {sl_pips}"
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