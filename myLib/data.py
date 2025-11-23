#--------------------------------------------------------------------------------- Location
# myLib/data.py

#--------------------------------------------------------------------------------- Description
# data

#--------------------------------------------------------------------------------- Import
from itertools import count
import inspect, time
import utils as utils
from debug import debug
from model import model_output

#--------------------------------------------------------------------------------- Action
class Data:
    #--------------------------------------------- init
    def __init__(self, log, db):
        #--------------------Variable
        self.this_class = self.__class__.__name__
        #--------------------Instance
        self.db = db
        self.log = log

    #--------------------------------------------- get_max_min
    def get_max_min(self, instrument, timeframe, mode, filed):
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
        #-------------- Variable
        start_time = time.time()
        #-------------- Data
        tblName = utils.get_tbl_name(instrument, timeframe)
        if mode == "max" : query = f"SELECT max({filed}) FROM {tblName}"
        if mode == "min" : query = f"SELECT min({filed}) FROM {tblName}"
        #--------------Action
        try:
            output.data = self.db.getDataOne(query)
            output.message["Time"] = int(time.time() - start_time)
            output.message["instrument"] = instrument
            output.message["timeframe"] = timeframe
            output.message["mode"] = mode
            output.message["filed"] = filed
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
    
    #--------------------------------------------- save
    def save(self, instrument, timeframe, data, bulk=False):
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
        #-------------- Variable
        start_time = time.time()
        iter = 0 
        insert = 0
        #-------------- Data
        tblName = utils.get_tbl_name(instrument, timeframe)
        if timeframe == "t1":
            query = f'INSERT INTO {tblName} (date, bid, ask) VALUES '
        else:
            query = f'INSERT INTO {tblName} (date, bidopen, bidclose, bidhigh, bidlow, askopen, askclose, askhigh, asklow) VALUES '
        #--------------Action
        try:
            if timeframe == "t1":
                if bulk :
                    data = data.drop_duplicates(subset=["Date"], keep="first")
                    for index, row in data.iloc[::-1].iterrows(): 
                        query += f"('{row['Date']}',{row['Bid']},{row['Ask']}),"
                        iter += 1
                        insert += 1
                    if iter > 0 : query = query[:-1]
                    output.status = self.db.execute(query)
                    if not output.status : insert = 0
                else:
                    for index, row in data.iloc[::-1].iterrows(): 
                        q = query + (f"('{row['Date']}',{row['Bid']},{row['Ask']})")
                        iter += 1
                        if self.db.execute(q) : 
                            insert += 1
                        else:
                            pass
            else:
                if bulk :
                    for index, row in data.iloc[::-1].iterrows(): 
                        query += f"('{row['Date']}',{row['BidOpen']},{row['BidClose']},{row['BidHigh']},{row['BidLow']},{row['AskOpen']},{row['AskClose']},{row['AskHigh']},{row['AskLow']}),"
                        iter += 1
                        insert += 1
                    if iter > 0 : query = query[:-1]
                    output.status = self.db.execute(query)
                    if not output.status : insert = 0
                else:
                    for index, row in data.iloc[::-1].iterrows(): 
                        q = query + (f"('{row['Date']}',{row['BidOpen']},{row['BidClose']},{row['BidHigh']},{row['BidLow']},{row['AskOpen']},{row['AskClose']},{row['AskHigh']},{row['AskLow']})")
                        iter += 1
                        if self.db.execute(q) : insert += 1
            output.message = f"{utils.sort(int(time.time() - start_time), 3)} | {instrument} | {timeframe} | {utils.sort(insert, 6)} ss|"
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{self.this_class}  | {this_method}", output.message)
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
