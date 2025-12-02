#--------------------------------------------------------------------------------- Location
# strategy/st01.py

#--------------------------------------------------------------------------------- Description
# st01

#--------------------------------------------------------------------------------- Import
import inspect, time, os,sys
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, f"{root_dir}/myLib")
from myLib.model import model_output
from myLib.utils import config, debug, sort
from myLib.log import Log
from myLib.forex import Forex

#--------------------------------------------------------------------------------- Action
class ST01:
    #--------------------------------------------- init
    def __init__(self, forex:Forex, symbol, amount, tp_pips, st_pips):
        #--------------------Debug
        self.this_class = self.__class__.__name__
        #--------------------Variable
        self.forex = forex
        self.symbol = symbol
        self.amount = amount
        self.tp_pips = tp_pips
        self.st_pips = st_pips
        #--------------------Instance
        self.log = Log()

    #--------------------------------------------- login
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
        output = model_output()
        start_time = time.time()

        try:
            #--------------Action
            result_buy = self.forex.trade_open(action="buy", symbol=self.symbol, amount=self.amount, tp_pips=self.tp_pips, sl_pips=self.st_pips)
            result_sell = self.forex.trade_open(action="sell", symbol=self.symbol, amount=self.amount, tp_pips=self.tp_pips, sl_pips=self.st_pips)
            #--------------Output
            output.message = {
                "method": this_method,
                "buy": result_buy.status,
                "sell": result_sell.status, 
                "Time": sort(int(time.time() - start_time), 3)
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

    #--------------------------------------------- logout
    def close(self):
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
            #--------------Action
            self.fx.logout()
            #--------------Output
            output.message = {
                "Time": sort(int(time.time() - start_time), 3),
                "account": self.account,
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