#--------------------------------------------------------------------------------- Location
# code/myLib/implementation.py

#--------------------------------------------------------------------------------- Description
# Implementation

#--------------------------------------------------------------------------------- Import
import inspect, time

from fastapi import params
from sqlalchemy import desc
from myLib.model import model_output
from myLib.logic_global import config, debug, log_instance, data_instance, forex_apis
from myLib.utils import sort
from myLib.log import Log
from myLib.data_orm import Data_Orm
from myLib.data_sql import Data_SQL
from myModel import *

#--------------------------------------------------------------------------------- Managemnet
class Implementation_Management:
    #-------------------------- [Init]
    def __init__(
            self,
            data_orm:Data_Orm=None, 
            data_sql:Data_SQL=None,
            log:Log=None
        ):
        #-------------- Variable
        self.this_class = self.__class__.__name__
        #-------------- Instance
        self.log = log if log else log_instance
        self.data_orm = data_orm if data_orm else data_instance["management_orm"]
        self.data_sql = data_sql if data_sql else data_instance["management_sql"]

    #--------------------------------------------- create_all_table
    def create_all_table(self):
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

        try:
            self.data_orm.create_all_tables()
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.message = f"Tables created"
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

    #--------------------------------------------- truncate_all_table
    def truncate_all_table(self):
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

        try:
            self.data_orm.truncate_all_table()
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.message = f"Tables Truncate"
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
    
    #--------------------------------------------- instrument
    def instrument(self, drop=False, truncate=False,  create=True, add=True):
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
        model = model_instrument_db
        #-------------- Data
        cfgData = config.get("instrument", {})
        defaultSymbols = cfgData.get("defaultSymbols")

        try:
            #-------------- Drop
            if drop : self.data_orm.drop(model=model)
            #-------------- Create
            if create : self.data_orm.create(model=model)
            #-------------- Truncate
            if truncate : self.data_orm.truncate(model=model)
            #-------------- Add
            if add:
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
                    self.data_orm.add(model=model_instrument_db, item=obj)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.message = f"Drop:{drop} | Create:{create} | Truncate:{truncate} | Add:{add}"
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

    #--------------------------------------------- instrument
    def account(self, drop=False, truncate=False,  create=True, add=True):
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
        model = model_account_db
        #-------------- Data
        try:
            #-------------- Drop
            if drop : self.data_orm.drop(model=model)
            #-------------- Create
            if create : self.data_orm.create(model=model)
            #-------------- Truncate
            if truncate : self.data_orm.truncate(model=model)
            #-------------- Add
            if add:
                obj = model(name='acc-trade', broker='FXCM', type='Demo', currency='USD', server='FXCM-USDDemo02', username='52035533', password='iaee0at', description="", enable=True)
                self.data_orm.add(model=model, item=obj)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.message = f"Drop:{drop} | Create:{create} | Truncate:{truncate} | Add:{add}"
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

    #--------------------------------------------- strategy
    def strategy(self, drop=False, truncate=False,  create=True, add=True):
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
        model = model_strategy_db

        try:
            #-------------- Drop
            if drop : self.data_orm.drop(model=model)
            #-------------- Create
            if create : self.data_orm.create(model=model)
            #-------------- Truncate
            if truncate : self.data_orm.truncate(model=model)
            #-------------- Add
            if add: 
                self.data_orm.add(model=model, item=model(name='ST_01', description='Buy|Sell   if p>0 same   if p<0 inverse'))
                self.data_orm.add(model=model, item=model(name='ST_02', description=''))
                self.data_orm.add(model=model, item=model(name='ST_03', description=''))
                self.data_orm.add(model=model, item=model(name='ST_04', description=''))
                self.data_orm.add(model=model, item=model(name='ST_05', description=''))
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.message = f"Drop:{drop} | Create:{create} | Truncate:{truncate} | Add:{add}"
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

    #--------------------------------------------- strategy_item
    def strategy_item(self, drop=False, truncate=False,  create=True, add=True):
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
        model = model_strategy_item_db
        #-------------- Data
        try:
            #-------------- Drop
            if drop : self.data_orm.drop(model=model)
            #-------------- Create
            if create : self.data_orm.create(model=model)
            #-------------- Truncate
            if truncate : self.data_orm.truncate(model=model)
            #-------------- Add
            if add:
                self.data_orm.add(model=model, item=model(name='buy', strategy_id=1, params="{'symbol':'EUR/USD','action':'buy','amount':10000,'tp_pips':10,'st_pips':10}", description="Start buy"))
                self.data_orm.add(model=model, item=model(name='sell', strategy_id=1, params="{'symbol':'EUR/USD','action':'sell','amount':10000,'tp_pips':10,'st_pips':10}", description="Start sell"))
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.message = f"Drop:{drop} | Create:{create} | Truncate:{truncate} | Add:{add}"
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

    #--------------------------------------------- live_execute
    def live_execute(self, drop=False, truncate=False,  create=True, add=True):
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
        model = model_live_execute_db
        #-------------- Data
        try:
            #-------------- Drop
            if drop : self.data_orm.drop(model=model)
            #-------------- Create
            if create : self.data_orm.create(model=model)
            #-------------- Truncate
            if truncate : self.data_orm.truncate(model=model)
            #-------------- Add
            if add:
                self.data_orm.add(model=model, item=model(name="test-1", strategy_item_id=1, account_id=1))
                self.data_orm.add(model=model, item=model(name="test-1", strategy_item_id=2, account_id=1))
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.message = f"Drop:{drop} | Create:{create} | Truncate:{truncate} | Add:{add}"
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
        self.data = Data_Orm()
    
    #--------------------------------------------- instrument
    def instrument(self, drop=False, truncate=False,  create=True, add=True):
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
        model = model_account_db
        #-------------- Data
        cfgData = config.get("instrument", {})
        defaultSymbols = cfgData.get("defaultSymbols")

        try:
            #-------------- Drop
            if drop : self.data_orm.drop(model=model)
            #-------------- Create
            if create : self.data_orm.create(model=model)
            #-------------- Truncate
            if truncate : self.data_orm.truncate(model=model)
            #-------------- Add
            if add:
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
                    self.data_orm.add(model=model_instrument_db, item=obj)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.message = f"Drop:{drop} | Create:{create} | Truncate:{truncate} | Add:{add}"
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

    #--------------------------------------------- instrument
    def account(self, drop=False, truncate=False,  create=True, add=True):
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
        model = model_account_db
        #-------------- Data
        try:
            #-------------- Drop
            if drop : self.data_orm.drop(model=model)
            #-------------- Create
            if create : self.data_orm.create(model=model)
            #-------------- Truncate
            if truncate : self.data_orm.truncate(model=model)
            #-------------- Add
            if add:
                obj = model(name='acc-history1', broker='FXCM', type='Demo', currency='USD', server='FXCM-USDDemo02', username='52030299', password='2idfycj', description="", enable=True)
                self.data_orm.add(model=model, item=obj)
                obj = model(name='acc-history2', broker='FXCM', type='Demo', currency='USD', server='FXCM-USDDemo02', username='52032860', password='aq8iwnf', description="", enable=True)
                self.data_orm.add(model=model, item=obj)
                obj = model(name='acc-live', broker='FXCM', type='Demo', currency='USD', server='FXCM-USDDemo02', username='52035533', password='iaee0at', description="", enable=True)
                self.data_orm.add(model=model, item=obj)
                obj = model(name='acc-trade', broker='FXCM', type='Demo', currency='USD', server='FXCM-USDDemo02', username='52035534', password='fjf0tzq', description="", enable=True)
                self.data_orm.add(model=model, item=obj)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.message = f"Drop:{drop} | Create:{create} | Truncate:{truncate} | Add:{add}"
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

    #--------------------------------------------- strategy
    def strategy(self, drop=False, truncate=False,  create=True, add=True):
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
        model = model_strategy_db
        #-------------- Data
        try:
            #-------------- Drop
            if drop : self.data_orm.drop(model=model)
            #-------------- Create
            if create : self.data_orm.create(model=model)
            #-------------- Truncate
            if truncate : self.data_orm.truncate(model=model)
            #-------------- Add
            if add:
                obj = model(name='strategy_01')
                self.data_orm.add(model=model, item=obj)
                obj = model(name='strategy_02')
                self.data_orm.add(model=model, item=obj)
                obj = model(name='strategy_03')
                self.data_orm.add(model=model, item=obj)
                obj = model(name='strategy_04')
                self.data_orm.add(model=model, item=obj)
                obj = model(name='strategy_05')
                self.data_orm.add(model=model, item=obj)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.message = f"Drop:{drop} | Create:{create} | Truncate:{truncate} | Add:{add}"
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

    #--------------------------------------------- strategy_item
    def strategy_item(self, drop=False, truncate=False,  create=True, add=True):
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
        model = model_strategy_item_db
        #-------------- Data
        try:
            #-------------- Drop
            if drop : self.data_orm.drop(model=model)
            #-------------- Create
            if create : self.data_orm.create(model=model)
            #-------------- Truncate
            if truncate : self.data_orm.truncate(model=model)
            #-------------- Add
            if add:
                params = "{'symbol': 'EUR/USD','amount': 10000,'tp_pips': 1,'st_pips': 10}"
                obj = model(name='st_01_itm_01', strategy_id=1, params=params)
                self.data_orm.add(model=model, item=obj)
                obj = model(name='st_02_itm_01', strategy_id=2, params=params)
                self.data_orm.add(model=model, item=obj)
                obj = model(name='st_03_itm_01', strategy_id=3, params=params)
                self.data_orm.add(model=model, item=obj)
                obj = model(name='st_04_itm_01', strategy_id=4, params=params)
                self.data_orm.add(model=model, item=obj)
                obj = model(name='st_05_itm_01', strategy_id=5, params=params)
                self.data_orm.add(model=model, item=obj)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.message = f"Drop:{drop} | Create:{create} | Truncate:{truncate} | Add:{add}"
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
        cfgData = config.get("instrument", {})
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
        tbl_instrument = config["instrument"]["table"]
        timeframes =config["timeframe"]
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