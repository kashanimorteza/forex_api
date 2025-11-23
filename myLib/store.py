#--------------------------------------------------------------------------------- Location
# myLib/store.py

#--------------------------------------------------------------------------------- Description
# Store

#--------------------------------------------------------------------------------- Import
import inspect, time
import utils as utils
from debug import debug
from model import model_output
from log import Log
from forexconnect_api import Forex
from myLib.data import Data

#--------------------------------------------------------------------------------- Action
class Store:
    #--------------------------------------------- init
    def __init__(self, log:Log, data:Data, forex:Forex):
        #--------------------Variable
        self.this_class = self.__class__.__name__
        #--------------------Instance
        self.log = log
        self.data = data
        self.forex = forex

    #--------------------------------------------- run
    def run(self, instrument, timeframe, mode, count, repeat, delay, save, bulk, datefrom, dateto):
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
        #-------------- Display
        params = {"instrument": instrument, "timeframe": timeframe, "mode": mode, "count": count, "repeat": repeat, "delay": delay, "save": save, "bulk": bulk, "datefrom": datefrom, "dateto": dateto}
        print(utils.format_dict_block("Store", params))
        #-------------- Action
        try:
            while(True):
                for r in range(repeat):
                    start = datefrom
                    end = dateto
                    while(True):
                        if end > start:
                            history:model_output = self.forex.history(instrument, timeframe, datefrom=start, dateto=end, count=count)
                            if history.status:
                                if save : self.data.save(instrument=instrument, timeframe=timeframe, data=history.data, bulk=bulk)
                                if mode == "complete" : 
                                    end = utils.timeframe_nex_date(mode ="complete", date=history.data["Date"].iloc[0] , timeframe=timeframe)
                                if mode == "up" : 
                                    start = utils.timeframe_nex_date(mode ="up", date=history.data["Date"].iloc[-1] , timeframe=timeframe)
                                if mode == "down" : 
                                    end = utils.timeframe_nex_date(mode ="down", date=history.data["Date"].iloc[0] , timeframe=timeframe)
                                if mode == "once" : 
                                    break
                            else : break
                            time.sleep(2)
                        else: break
                if delay == 0: break; 
                time.sleep(delay)
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{self.this_class} | {this_method}", output.message)
            #--------------Log
            if log : self.log.log(log_model, output)
            #--------------Output
            return output
        except Exception as e:  
            #--------------Error
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
