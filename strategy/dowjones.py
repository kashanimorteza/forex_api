#--------------------------------------------------------------------------------- Location
# strategy/dowjones.py

#--------------------------------------------------------------------------------- Description
# dowjones

#--------------------------------------------------------------------------------- Import
import inspect, time
from datetime import datetime, timezone
import pytz
from logic.startup import debug, log_instance, Strategy_Run, list_instrument
from logic.util import model_output, sort
from logic.log import Logic_Log

#--------------------------------------------------------------------------------- Action
class Dowjones:
    #--------------------------------------------- init
    def __init__(self, params:dict=None, log:Logic_Log=None):
        #-------------- Debug
        self.this_class = self.__class__.__name__
        #-------------- Instance
        self.log = log if log else log_instance
        #-------------- Params
        self.symbols = params.get("symbols").split(',')
        self.actions = params.get("actions").split(',')
        self.amount = params.get("amount")
        self.tp_pips = params.get("tp_pips")
        self.sl_pips = params.get("sl_pips")
        self.limit_trade = int(params.get("limit_trade"))
        self.limit_profit = int(params.get("limit_profit"))
        self.limit_loss = int(params.get("limit_loss"))
        self.params = params.get("params")
        self.time_start = datetime.strptime(self.params.get("time_start"), "%H:%M:%S").time()
        self.time_end = datetime.strptime(self.params.get("time_end"), "%H:%M:%S").time()
        self.change_pip = self.params.get("change_pip")
        self.order_pip = self.params.get("order_pip")
        self.down = self.params.get("down")
        self.up = self.params.get("up")
        self.pending_limit = self.params.get("pending_limit")
        #-------------- Variable
        self.set_order = None
        self.set_price = None
        self.date = None
        self.ask = None
        self.bid = None
        self.price = None
        
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
        #--------------Action
        try:
            pass
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
        if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 15)} | {output.time}", output.message)
        #--------------Log
        if log : self.log.log(log_model, output)
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
        #--------------Action
        try:
            items.append({"run": Strategy_Run.ORDER_CLOSE_ALL})
        except Exception as e:  
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Output
        output.time = sort(f"{(time.time() - start_time):.3f}", 3)
        output.data = items
        output.message = output.status
        #--------------Verbose
        if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 15)} | {output.time}", output.message)
        #--------------Log
        if log : self.log.log(log_model, output)
        #--------------Return
        return output
    
    #--------------------------------------------- order_close
    def order_close(self, order_detaile):
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
            pass
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
        if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 15)} | {output.time}", output.message)
        #--------------Log
        if log : self.log.log(log_model, output)
        #--------------Return
        return output

    #--------------------------------------------- price_change
    def price_change(self, price_data, order_close, order_open, order_pending):
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
        #--------------Action
        try:
            for item in price_data:
                #---------Data
                symbol = item
                digits = price_data[symbol]["digits"]
                date = price_data[symbol]["date"]
                ask = price_data[symbol]["ask"]
                bid = price_data[symbol]["bid"]
                #---------Everyday
                if (self.set_order is None) or (self.set_order is False) or ( date.date()> self.date.date()):
                    ny_date = self.time_change_utc_newyork(date)
                    #---------Time
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
                            disagreement = abs((ask - self.ask) * (10 ** digits))
                            if disagreement >= self.change_pip:
                                self.set_order = True
                                self.set_price = False
                                action = self.up if ask > self.ask else self.down
                                item = {
                                    "run": Strategy_Run.ORDER_PENDING,
                                    "date": date,
                                    "symbol": symbol, 
                                    "action": action, 
                                    "amount": self.amount, 
                                    "ask": self.ask-(self.order_pip / (10 ** digits)),
                                    "bid": self.bid+(self.order_pip / (10 ** digits)), 
                                    "tp_pips": self.tp_pips, 
                                    "sl_pips": self.sl_pips,
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
        if verbose : self.log.verbose("rep", f"{sort(self.this_class, 15)} | {sort(this_method, 15)} | {output.time}", output.message)
        #--------------Log
        if log : self.log.log(log_model, output)
        #--------------Return
        return output
    
    #--------------------------------------------- time_change_utc_newyork
    def time_change_utc_newyork(self, date):
        #--------------Action
        utc = pytz.utc
        ny = pytz.timezone("America/New_York")
        utc_dt = utc.localize(date)
        output = utc_dt.astimezone(ny)
        #--------------Return
        return output