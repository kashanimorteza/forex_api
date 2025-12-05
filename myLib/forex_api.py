#--------------------------------------------------------------------------------- Location
# myLib/forex_api.py

#--------------------------------------------------------------------------------- Description
# forexconnect

#--------------------------------------------------------------------------------- Import
import inspect, time
from model import model_output
from utils import config, debug, sort
from forexconnect import ForexConnect, fxcorepy
from myLib.log import Log

#--------------------------------------------------------------------------------- Action
class Forex_Api:
    #--------------------------------------------- init
    def __init__(self, account=None):
        #--------------------Variable
        self.this_class = self.__class__.__name__
        #--------------------Instance
        self.log = Log()
        self.fx = ForexConnect()
        #--------------------Data
        self.account = account
        self.id = None
        self.server = config['forex_connect'][account]['server']
        self.username = config['forex_connect'][account]['username']
        self.password = config['forex_connect'][account]['password']
        self.url = config['forex_connect'][account]['url']
        self.key = config['forex_connect'][account]['key']

    #--------------------------------------------- on_status_changed
    def session_status_changed(self, session: fxcorepy.O2GSession, status: fxcorepy.AO2GSessionStatus.O2GSessionStatus):
        print("Trading session status: " + str(status))

    #--------------------------------------------- login
    def login(self):
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

        try:
            #--------------Variable
            start_time = time.time()
            #--------------Action
            self.fx.login(self.username, self.password, self.url, self.server, self.session_status_changed)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.message = self.account
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

    #--------------------------------------------- logout
    def logout(self):
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

        try:
            #--------------Variable
            start_time = time.time()
            #--------------Action
            self.fx.logout()
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.message = self.account
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