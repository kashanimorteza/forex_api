#--------------------------------------------------------------------------------- Location
# myLib/forex_api.py

#--------------------------------------------------------------------------------- Description
# forex_api

#--------------------------------------------------------------------------------- Import
import inspect, time
from myLib.model import model_output
from myLib.logic_global import debug, log_instance
from myLib.utils import sort
from myLib.log import Log
from forexconnect import ForexConnect, fxcorepy

#--------------------------------------------------------------------------------- Action
class Forex_Api:
    #--------------------------------------------- init
    def __init__(self, name=None, type=None, username=None, password=None, url=None, key=None, log=None):
        #--------------------Variable
        self.this_class = self.__class__.__name__
        self.id = None
        self.name = name
        self.type = type
        self.username = username
        self.password = password
        self.url = url
        self.key = key
        self.balance = None
        self.equity = None
        #--------------------Instance
        self.log:Log = log if log else log_instance
        self.fx = ForexConnect()

    #--------------------------------------------- on_status_changed
    def session_status_changed(self, session: fxcorepy.O2GSession, status: fxcorepy.AO2GSessionStatus.O2GSessionStatus):
        print("Trading session status: " + str(status))

    #--------------------------------------------- login
    def login(self):
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
            self.fx.login(self.username, self.password, self.url, self.type, self.session_status_changed)
            self.info()
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = None
            output.message= self.name
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

    #--------------------------------------------- logout
    def logout(self):
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
            self.fx.logout()
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = None
            output.message= self.name
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

    #--------------------------------------------- logout
    def info(self):
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
            accounts_table = self.fx.get_table(ForexConnect.ACCOUNTS)
            for account in accounts_table:
                self.id = account.account_id
                self.balance = account.balance
                self.equity = account.equity
                break
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.data = account
            output.message= f"{self.name} | {self.id} | Balance: {self.balance} | Equity: {self.equity}"
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