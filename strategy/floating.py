#--------------------------------------------------------------------------------- Location
# strategy/floating.py

#--------------------------------------------------------------------------------- Description
# floating

#--------------------------------------------------------------------------------- Import
import inspect, time
from logic.startup import debug, log_instance, Strategy_Run
from logic.util import model_output, sort
from logic.log import Logic_Log

#--------------------------------------------------------------------------------- Action
class Floating:
    #--------------------------------------------- init
    def __init__(self, params:dict=None, log:Logic_Log=None):
        #-------------- Variable
        self.this_class = self.__class__.__name__
        self.params = params
        #-------------- Instance
        self.log = log if log else log_instance
        #-------------- Params
        self.symbols = self.params.get("symbols").split(',')
        self.actions = self.params.get("actions").split(',')
        self.amount = self.params.get("amount")
        self.tp_pips = self.params.get("tp_pips")
        self.sl_pips = self.params.get("sl_pips")
        self.limit_trade = int(self.params.get("limit_trade"))
        self.limit_profit = int(self.params.get("limit_profit"))
        self.limit_loss = int(self.params.get("limit_loss"))
        
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
        #--------------Variable
        items = []
        
        try:
            #--------------Action
            for symbol in self.symbols :
                for action in self.actions :
                    item = {
                        "run": Strategy_Run.ORDER_OPEN, 
                        "state": this_method,
                        "action": action, 
                        "symbol": symbol, 
                        "amount": self.amount, 
                        "tp_pips": self.tp_pips, 
                        "sl_pips": self.sl_pips
                        }
                    items.append(item)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 7)
            output.data = items
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
        #--------------Variable
        items = []

        try:
            #--------------Action
            item = {
                "run": Strategy_Run.ORDER_CLOSE_ALL, 
                "state": this_method
            }
            items.append(item)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 7)
            output.data = items
            output.message = output.status
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 25)} | {output.time}", output.message)
            output.data = items
            output.message = None
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
        #--------------Variable
        items = []

        try:
            #--------------Data
            symbol = order_detaile.get("symbol")
            action = order_detaile.get("action")
            amount = order_detaile.get("amount")
            profit = order_detaile.get("profit")
            trade_id = order_detaile.get("trade_id")
            #--------------Rule
            if profit < 0 :
                action = "sell" if action == "buy" else "buy"
            #--------------Action
            item = {
                "run": Strategy_Run.ORDER_OPEN,
                "state": this_method,
                "symbol": symbol, 
                "action": action, 
                "amount": amount, 
                "tp_pips": self.tp_pips, 
                "sl_pips": self.sl_pips
            }
            items.append(item)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 7)
            output.data = items
            output.message = f"{trade_id} | {action}:{profit} | {symbol},{amount},{self.tp_pips},{self.sl_pips}"
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

    #--------------------------------------------- price_change
    def price_change(self, price_detailes, order_detailes):
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
        #--------------Variable
        items = []

        try:
            #--------------Data
            #--------------Rule
            #--------------Action
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 7)
            output.data = items
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