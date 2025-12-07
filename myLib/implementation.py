#--------------------------------------------------------------------------------- Location
# code/myLib/implementation.py

#--------------------------------------------------------------------------------- Description
# Implementation

#--------------------------------------------------------------------------------- Import
import inspect, time
import myLib.utils as utils
from myLib.debug import debug
from myLib.model import model_output
from myLib.log import Log
from myLib.data_orm import Data_Orm
from myModel import *
from myModel.model_instrument import model_instrument_db
from myLib.forex import Forex
from myLib.utils import debug, sort, format_dict_block, timeframe_nex_date

#--------------------------------------------------------------------------------- Action
class Implementation:
    #---------------------------------------- init
    def __init__(self, log=None, db=None):
        #--------------------Variable
        self.this_class = self.__class__.__name__
        #--------------------log
        self.log = Log() if log is None else log
        #--------------------database
        self.db = db
    
    #--------------------------------------------- instrument
    def instrument(self, drop=None, create=None, add=None):
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
        #-------------- Variable
        data_orm = Data_Orm()
        #-------------- Data
        cfgData = utils.config.get("instrument", {})
        defaultSymbols = cfgData.get("defaultSymbols")

        try:
            for instrument in defaultSymbols:
                name = instrument.replace('/', '')
                name = name.replace('.', '')
                category = 100
                priority = 100
                if instrument == "XAU/USD" : 
                    category = 1
                    priority = 1 
                if instrument == "XAG/USD" : 
                    category = 1
                    priority = 2
                if instrument == "USOil" : 
                    category = 1
                    priority = 3
                if instrument == "UKOil" : 
                    category = 1
                    priority = 4
                if instrument == "EUR/USD" : 
                    category = 1
                    priority = 5
                obj = model_instrument_db(name=name, instrument=instrument,  category=category,  priority=priority, description="", enable=True)
                data_orm.add(model=model_instrument_db, item=obj)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.message =len(defaultSymbols)
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
    
    #--------------------------------------------- set_instrument_category
    def set_instrument_category(self, instrument, category):
        #-------------------- Description
        # IN     : 
        # OUT    : 
        # Action : Set category for instrument
        #-------------------- Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        output = model_output()
        #-------------------- Variable
        cfgData = utils.config.get("instrument", {})
        tblName = cfgData.get("table")
        #-------------------- Action
        try:
            output.data = self.db.execute(f"UPDATE {tblName} SET category={category} WHERE instrument='{instrument}';")
        except Exception as e:  
            #--------------Error
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Verbose
        if verbose : print(output)
        #--------------Log
        if log : self.log.log(log_model, output)
        #--------------Output
        return output

    #--------------------------------------------- create_instrument_timeframe_table
    def create_instrument_timeframe_table(self, drop=None, create=None):
        #-------------------- Description
        # IN     : 
        # OUT    : 
        # Action : Create data table for each instrument and timeframe
        #-------------------- Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        output = model_output()
        #-------------------- Variable
        tbl_instrument = utils.config["instrument"]["table"]
        timeframes =utils.config["timeframe"]
        #-------------------- Action
        try:
            tblList = self.db.getData(f"SELECT name FROM {tbl_instrument}")
            for i in tblList:
                for t in timeframes:
                    tblName =f"{i[0]}_{t}"
                    if t =="t1":
                        query = f"""
                            CREATE TABLE IF NOT EXISTS {tblName} (
                                id SERIAL UNIQUE NOT NULL,
                                date TIMESTAMP UNIQUE NOT NULL PRIMARY KEY,
                                bid real,
                                ask real                            
                            )"""
                    else:                  
                        query = f"""
                            CREATE TABLE IF NOT EXISTS {tblName} (
                                id SERIAL UNIQUE NOT NULL,
                                date TIMESTAMP UNIQUE NOT NULL PRIMARY KEY,
                                bidopen real,
                                bidclose real,
                                bidhigh real,
                                bidlow real,
                                askopen real,
                                askclose real,
                                askhigh real,
                                asklow real,
                                tickqty smallint
                            )"""
                    if drop:
                        output.data["drop"] = self.db.execute(f"DROP TABLE IF EXISTS {tblName}")
                        self.log.log('not',f'{self.this_class}({this_method})', f'Drop table {tblName} : {output.data["drop"]}')
                    if create:
                        output.data["create"] = self.db.execute(query)
                        self.log.log('not',f'{self.this_class}({this_method})', f'Create table {tblName} : {output.data["create"]}')
        except Exception as e:  
            #--------------Error
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Verbose
        if verbose : print(output)
        #--------------Log
        if log : self.log.log(log_model, output)
        #--------------Output
        return output
    
    #--------------------------------------------- drop_all_table
    def drop_all_table(self):
        #-------------------- Description
        # IN     : 
        # OUT    : 
        # Action : Create instrument table and fill it with data 
        #-------------------- Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        output = model_output()
        #-------------------- Variable
        query = f"""DO
        $$
        DECLARE
            r RECORD;
        BEGIN
            FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public')
            LOOP
                EXECUTE 'DROP TABLE IF EXISTS public.' || quote_ident(r.tablename) || ' CASCADE';
            END LOOP;
        END;
        $$;"""
        #-------------------- Execute
        try:
            output.data = self.db.execute(query)
            self.log.log('not',f'{self.this_class}({this_method})', f'Drop All : {output.data}')
        except Exception as e:  
            #--------------Error
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Verbose
        if verbose : print(output)
        #--------------Log
        if log : self.log.log(log_model, output)
        #--------------Output
        return output