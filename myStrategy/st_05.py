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
from myLib.fxcm_api import Forex
from myModel.model_live_order import model_live_order_db

#--------------------------------------------------------------------------------- Action
class ST_05:
    #--------------------------------------------- init
    def __init__(
            self,
            forex:Forex=None,
            params=None,
            data_orm:Data_Orm=None, 
            data_sql:Data_SQL=None,
            log:Log=None
        ):
        #-------------- Variable
        self.this_class = self.__class__.__name__
        self.id = 5
        self.forex = forex
        #-------------- Instance
        self.log = log if log else log_instance
        self.data_orm = data_orm if data_orm else data_instance["management_orm"]
        self.data_sql = data_sql if data_sql else data_instance["management_sql"]
        #-------------- Params
        self.symbol = params["symbol"]
        self.action = params["action"]
        self.amount = int(params["amount"])
        self.tp_pips = int(params["tp_pips"])
        self.st_pips = int(params["st_pips"])

    #--------------------------------------------- start
    def start(self, execute_id:int):
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
            result:model_output = self.forex.trade_open(action=self.action, symbol=self.symbol, amount=self.amount, tp_pips=self.tp_pips, sl_pips=self.st_pips, execute_id=execute_id)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = None
            output.message = {self.action: result.status}
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

    #--------------------------------------------- end
    def end(self, execute_id:int):
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
        #--------------Variable
        order_ids = []

        try:
            #--------------Data
            orders:list[model_live_order_db] = self.data_orm.items(model=model_live_order_db, execute_id=execute_id, status='open').data
            for order in orders:
                order_ids.append(order.order_id)
            #--------------Action
            result:model_output = self.forex.order_close_all(order_ids=order_ids)
            #--------------Update
            if result.status:
                for order in orders:
                    order.status = 'close'
                    self.data_orm.update(model=model_live_order_db, item=order)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = None
            output.message = {
                "Orders": len(order_ids),
                "Close": result.message["Close"]
            }
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
    def order_close(self, order_detail):
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
            pass
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = order_detail
            output.message = None
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
            pass
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = order_detail
            output.message = None
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