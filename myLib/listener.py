#--------------------------------------------------------------------------------- Location
# myLib/listener.py

#--------------------------------------------------------------------------------- Description
# listener

#--------------------------------------------------------------------------------- Import
import ast
import inspect, time
from model import model_output
from myLib.utils import debug, sort
from myLib.data_orm import data_orm
from myModel.strategy_item import strategy_item_model_db
from myStrategy import *
from myLib.log import Log

#--------------------------------------------------------------------------------- Action
class Listener:
    #--------------------------------------------- init
    def __init__(self, forex):
        #--------------------Variable
        self.this_class = self.__class__.__name__
        self.forex = forex
        #--------------------Instance
        self.log = Log()
        self.data_orm = data_orm()

    #--------------------------------------------- trade_read
    def read_trade(self):
        #-------------- Description
        # IN     : 
        # OUT    : 
        # Action :
        #-------------- Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        output = model_output()
        start_time = time.time()
        
        try:
            #--------------Variable
            custom_id = 1
            #--------------Action
            self.strategy_next(custom_id)
            #--------------Output
            output.message = {
                "Time": sort(int(time.time() - start_time), 3),
            }
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{self.this_class} | {this_method}", output.message)
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

    #--------------------------------------------- strategy_next
    def strategy_next(self, custom_id):
        #-------------- Description
        # IN     : 
        # OUT    : 
        # Action :
        #-------------- Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        output = model_output()
        start_time = time.time()
        
        try:
            #--------------Variable
            item = self.data_orm.item(model=strategy_item_model_db, id=int(custom_id)).data[0]
            strategy_id = item.strategy_id
            params = item.params
            params = ast.literal_eval(item.params)
            #--------------Data
            if strategy_id ==1 : strategy = ST01(forex=self.forex, params=params)
            #--------------Action
            strategy.next()
            #--------------Output
            output.message = {
                "Time": sort(int(time.time() - start_time), 3),
            }
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{self.this_class} | {this_method}", output.message)
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