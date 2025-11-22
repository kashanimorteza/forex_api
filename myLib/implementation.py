#--------------------------------------------------------------------------------- Location
# code/myLib/implementation.py

#--------------------------------------------------------------------------------- Description
# Implementation

#--------------------------------------------------------------------------------- Import
import inspect
import myLib.utils as utils
from myLib.debug import debug
from myLib.model import model_output
from myLib.log import Log

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
    
    #--------------------------------------------- create_instrument_table
    def create_instrument_table(self, drop=None, create=None, add=None):
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
        count = 0
        cfgData = utils.config.get("instrument", {})
        tblName = cfgData.get("table")
        useDefaultSymbols = cfgData.get("useDefaultSymbols")
        defaultSymbols = cfgData.get("defaultSymbols")
        #-------------------- Execute
        try:
            if drop:
                output.data["drop"] = self.db.execute(f"DROP TABLE IF EXISTS {tblName}")
                self.log.log('not',f'{self.this_class}({this_method})', f'Drop   : {tblName} : {output.data["drop"]}')
            if create:
                query = f"""CREATE TABLE IF NOT EXISTS {tblName}
                (
                    id SERIAL UNIQUE NOT NULL,
                    name VARCHAR (50) UNIQUE NOT NULL PRIMARY KEY,
                    instrument VARCHAR (50),
                    category smallint DEFAULT 100
                )"""
                output.data["create"] = self.db.execute(query)
                self.log.log('not',f'{self.this_class}({this_method})', f'Create : {tblName} : {output.data["create"]}')
            if add:
                if useDefaultSymbols:
                    instruments = defaultSymbols 
                else:
                    from myLib.forexconnect_api import Forex
                    instruments = Forex().instruments()
                query = f'INSERT INTO {tblName} (name, instrument, category) VALUES '
                for i in instruments:
                    name = i.replace('/', '')
                    name = name.replace('.', '')
                    if self.db.getDataOne(f"SELECT id FROM {tblName} WHERE name='{name}'") is None:
                        query += f"('{name}' , '{i}', 5),"
                        count += 1
                if count > 0 :
                    query = query[:-1]
                    output.data["add"] = -1 if self.db.execute(query) is False else count
                else:
                    output.data["add"] = 0
                self.log.log('not',f'{self.this_class}({this_method})', f'Add    : {tblName} : {output.data["add"]}')
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