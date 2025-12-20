#--------------------------------------------------------------------------------- Location
# myStrategy/st_01.py

#--------------------------------------------------------------------------------- Description
# st_01

#--------------------------------------------------------------------------------- Import
import inspect, time
from myLib.logic_global import debug, log_instance
from myLib.utils import model_output, sort
from myLib.log import Log

#--------------------------------------------------------------------------------- Action
class Floating:
    #--------------------------------------------- init
    def __init__(self, params:dict=None, log:Log=None):
        #-------------- Variable
        self.this_class = self.__class__.__name__
        self.params = params
        #-------------- Instance
        self.log = log if log else log_instance
        
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
        params = self.params
        output.data = []
        
        try:
            #--------------Data
            actions = params.get("actions").split(',')
            symbols = params.get("symbols", "").split(',')
            amount = params.get("amount")
            tp_pips = params.get("tp_pips")
            sl_pips = params.get("sl_pips")
            #--------------Action
            for symbol in symbols :
                for action in actions :
                    output.data.append({
                        "run": "order_open",
                        "action": action,
                        "symbol": symbol,
                        "amount": amount,
                        "tp_pips": tp_pips,
                        "sl_pips": sl_pips,
                    })
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 12)} | {output.time}", output.message)
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
        params = self.params
        output.data = [dict]

        try:
            #--------------Data
            actions = params.get("actions").split(',')
            symbols = params.get("symbols", "").split(',')
            amount = params.get("amount")
            tp_pips = params.get("tp_pips")
            sl_pips = params.get("sl_pips")
            #--------------Action
            output.data.append({
                "run": "close_all_order",
                "state": this_method,
            })
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 12)} | {output.time}", output.message)
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
        output.data = []

        try:
            #--------------Data
            action = order_detaile.get("action")
            symbol = order_detaile.get("symbol")
            amount = order_detaile.get("amount")
            tp_pips = self.params.get("tp_pips")
            sl_pips = self.params.get("sl_pips")
            profit = order_detaile.get("profit")
            trade_id = order_detaile.get("trade_id")
            #--------------Rule
            if profit < 0 :
                action = "sell" if action == "buy" else "buy"
            #--------------Action
            output.data.append({
                "run": "order_open",
                "action": action,
                "symbol": symbol,
                "amount": amount,
                "tp_pips": tp_pips,
                "sl_pips": sl_pips,
            })
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.message = f"{trade_id} | {order_detaile.get('action')}:{profit} | {action},{symbol},{amount},{tp_pips},{sl_pips},{output.status}"
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 12)} | {output.time}", output.message)
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
    def price_change(self, order_detaile):
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
        output.data = [dict]

        try:
            #--------------Data
            action = order_detaile.get("action")
            symbol = order_detaile.get("symbol")
            amount = order_detaile.get("amount")
            tp_pips = self.params.get("tp_pips")
            sl_pips = self.params.get("st_pips")
            profit = order_detaile.get("profit")
            trade_id = order_detaile.get("trade_id")
            #--------------Rule
            if profit < 0 :
                action = "sell" if action == "buy" else "buy"
            #--------------Action
            output.data.append({
                "run": "order_open",
                "state": this_method,
                "buy_sell": action,
                "symbol": symbol,
                "amount": amount,
                "tp_pips": tp_pips,
                "sl_pips": sl_pips,
            })
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.message = f"{trade_id} | {order_detaile.get('action')}:{profit} | {action},{symbol},{amount},{tp_pips},{sl_pips},{output.status}"
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 12)} | {output.time}", output.message)
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