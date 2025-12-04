#--------------------------------------------------------------------------------- Location
# myStrategy/strategy_02.py

#--------------------------------------------------------------------------------- Description
# strategy_02

#--------------------------------------------------------------------------------- Import
from ast import mod
import inspect, time
from myLib.model import model_output
from myLib.utils import debug, sort
from myLib.log import Log

#--------------------------------------------------------------------------------- Action
class Strategy_02:
    #--------------------------------------------- init
    def __init__(self, forex, params):
        #--------------------Debug
        self.this_class = self.__class__.__name__
        #--------------------Variable
        self.id = 2
        self.item_id = params["item_id"]
        self.symbol = params["symbol"]
        self.amount = params["amount"]
        self.tp_pips = params["tp_pips"]
        self.st_pips = params["st_pips"]
        #--------------------Instance
        self.forex = forex
        self.log = Log()
    
    #--------------------------------------------- action
    def action(self, mode=None):
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
            if mode == "buy" or mode == "sell":
                self.forex.trade_open(action=mode, symbol=self.symbol, amount=self.amount, tp_pips=self.tp_pips, sl_pips=self.st_pips, strategy_item_id=self.item_id)
            elif mode == "both":
                self.forex.trade_open(action="buy", symbol=self.symbol, amount=self.amount, tp_pips=self.tp_pips, sl_pips=self.st_pips, strategy_item_id=self.item_id)
                self.forex.trade_open(action="sell", symbol=self.symbol, amount=self.amount, tp_pips=self.tp_pips, sl_pips=self.st_pips, strategy_item_id=self.item_id)
            elif mode == "close":
                self.forex.trade_close_all()
            #--------------Output
            output.time = sort(int(time.time() - start_time), 3)
            output.message = {
                "mode": mode,
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
        #-------------- Output
        output = model_output()
        output.class_name = self.this_class
        output.method_name = this_method
        #--------------Variable
        start_time = time.time()
        
        try:
            #--------------Action
            self.action(mode="buy")
            #--------------Output
            output.time = sort(int(time.time() - start_time), 3)
            output.message = {

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
    def next(self, params):
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
        terget = None
        #--------------Data
        order_id = params["order_id"]
        action = params["action"]
        profit = params["profit"]

        try:
            #--------------Action
            if action == "S":
                terget = "sell" if profit > 0 else "buy"
            if action == "B":
                terget = "buy" if profit > 0 else "sell"
            self.action(mode=terget)
            #--------------Output
            output.time = sort(int(time.time() - start_time), 3)
            output.message = {
                "order_id": order_id,
                "action": action,
                "profit": profit,
                "target": terget,
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