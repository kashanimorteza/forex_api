#--------------------------------------------------------------------------------- Location
# myStrategy/strategy_01.py

#--------------------------------------------------------------------------------- Description
# strategy_01

#--------------------------------------------------------------------------------- Import
import inspect, time
from myLib.model import model_output
from myLib.utils import debug, sort
from myLib.log import Log

#--------------------------------------------------------------------------------- Action
class Strategy_01:
    #--------------------------------------------- init
    def __init__(self, forex, params):
        #--------------------Debug
        self.this_class = self.__class__.__name__
        #--------------------Variable
        self.id = 1
        self.forex = forex
        self.symbol = params["symbol"]
        self.amount = params["amount"]
        self.tp_pips = params["tp_pips"]
        self.st_pips = params["st_pips"]
        #--------------------Instance
        self.log = Log()

    #--------------------------------------------- action
    def action(self, ac=False):
        #-------------- Description
        # IN     : 
        # OUT    : 
        # Action :
        #-------------- Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        #-------------- Output
        output = model_output()
        output.class_name = self.this_class
        output.method_name = this_method
        #--------------Variable
        start_time = time.time()
        
        try:
            #--------------Action
            result_buy = self.forex.trade_open(action="buy", symbol=self.symbol, amount=self.amount, tp_pips=self.tp_pips, sl_pips=self.st_pips, strategy_id=self.id, ac=ac)
            result_sell = self.forex.trade_open(action="sell", symbol=self.symbol, amount=self.amount, tp_pips=self.tp_pips, sl_pips=self.st_pips, strategy_id=self.id, ac=ac)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.message = {
                "buy": result_buy.status,
                "sell": result_sell.status
            }
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{self.this_class} | {this_method} | {output.time}", output.message)
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

    #--------------------------------------------- Next
    def next(self, order_id):
        #-------------- Description
        # IN     : 
        # OUT    : 
        # Action :
        #-------------- Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        #-------------- Output
        output = model_output()
        output.class_name = self.this_class
        output.method_name = this_method
        #--------------Variable
        start_time = time.time()

        try:
            #--------------Action
            self.action(ac=True)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.message = {
                "order_id": order_id,
            }
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{self.this_class} | {this_method} | {output.time}", output.message)
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