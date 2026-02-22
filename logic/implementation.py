#--------------------------------------------------------------------------------- Location
# logic/logic_implementation.py

#--------------------------------------------------------------------------------- Description
# Logic_Implementation

#--------------------------------------------------------------------------------- Import
import inspect, time
from logic.startup import config, debug, log_instance, data_instance, forex_apis
from logic.util import model_output, sort
from logic.log import Logic_Log
from logic.data_orm import Data_Orm
from logic.data_sql import Data_SQL
from logic.live import Logic_Live
from model import *

#--------------------------------------------------------------------------------- Managemnet
class Logic_Implementation:
    #-------------------------- [Init]
    def __init__(self, data_orm:Data_Orm=None, data_sql:Data_SQL=None, log:Logic_Log=None):
        #-------------- Variable
        self.this_class = self.__class__.__name__
        #-------------- Instance
        self.log = log if log else log_instance
        self.data_orm = data_orm if data_orm else data_instance["management_orm"]
        self.data_sql = data_sql if data_sql else data_instance["data_sql"]
    
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
            output.time = sort(f"{(time.time() - start_time):.3f}", 7)
            output.message = True
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 12)} | {sort(this_method, 35)} | {output.time}", output.message)
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
            output.time = sort(f"{(time.time() - start_time):.3f}", 7)
            output.message = True
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 12)} | {sort(this_method, 35)} | {output.time}", output.message)
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
        useDefaultSymbols = cfgData.get("useDefaultSymbols")
        if useDefaultSymbols :
            defaultSymbols = cfgData.get("defaultSymbols")
        else:
            from logic.startup import load_forex_api
            load_forex_api()
            forex:Logic_Live = forex_apis[2]
            offers = forex.get_table("OFFERS").data
        try:
            #-------------- Drop
            if drop : self.data_orm.drop(model=model)
            #-------------- Create
            if create : self.data_orm.create(model=model)
            #-------------- Truncate
            if truncate : self.data_orm.truncate(model=model)
            #-------------- Add
            if add:
                if useDefaultSymbols :
                    for instrument in defaultSymbols:
                        name = instrument.replace('/', '')
                        name = name.replace('.', '')
                        category = 1
                        priority = 1
                        obj = model_instrument_db(name=name, instrument=instrument,  category=category,  priority=priority, description="", enable=True)
                        self.data_orm.add(model=model_instrument_db, item=obj)
                else:
                    for offer in offers:
                        instrument = offer['instrument']
                        digits = offer['digits']
                        point_size = offer['point_size']
                        name = instrument.replace('/', '')
                        name = name.replace('.', '')
                        obj = model_instrument_db(name=name, instrument=instrument, description="", enable=True, digits=digits, point_size=point_size)
                        self.data_orm.add(model=model_instrument_db, item=obj)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 7)
            output.message = f"Drop:{drop} | Create:{create} | Truncate:{truncate} | Add:{add}"
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 12)} | {sort(this_method, 35)} | {output.time}", output.message)
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
                self.data_orm.add(model=model, item=model(name='back', broker='back', type='', currency='', server='', username='', password='', description="", enable=True))
                self.data_orm.add(model=model, item=model(name='live-demo', broker='FXCM', type='Demo', currency='USD', server='FXCM-USDDemo02', username='52047997', password='pdk2cnf', description="", enable=True))
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 7)
            output.message = f"Drop:{drop} | Create:{create} | Truncate:{truncate} | Add:{add}"
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 12)} | {sort(this_method, 35)} | {output.time}", output.message)
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
                self.data_orm.add(model=model, item=model(name='Dowjones', description='Every day at 16:30'))
                self.data_orm.add(model=model, item=model(name='OneWay', description='Buy|Sell'))
                self.data_orm.add(model=model, item=model(name='Floating', description='Buy&Sell   if p>0:same   if p<0:reverse'))
                self.data_orm.add(model=model, item=model(name='Ali_PoolBack', description=''))
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 7)
            output.message = f"Drop:{drop} | Create:{create} | Truncate:{truncate} | Add:{add}"
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 12)} | {sort(this_method, 35)} | {output.time}", output.message)
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
                #-------------- Dowjones
                #US30
                item =model(
                    name='US30',
                    strategy_id=1,
                    symbols='US30',
                    actions='buy,sell',
                    amount=1,
                    tp_pips=40, 
                    sl_pips=20,
                    params="{'time_start':'09:30:00', 'time_end':'09:30:15', 'change_pip': 10, 'order_pip': 5, 'down': 'buy', 'up': 'sell', 'pending_limit': 120}")
                self.data_orm.add(model=model, item=item)
                #XAU/USD
                item =model(
                    name='XAU/USD',
                    strategy_id=1,
                    symbols='XAU/USD',
                    actions='buy,sell',
                    amount=1,
                    tp_pips=40, 
                    sl_pips=20,
                    params="{'time_start':'09:30:00', 'time_end':'09:30:15', 'change_pip': 10, 'order_pip': 5, 'down': 'buy', 'up': 'sell', 'pending_limit': 120}")
                self.data_orm.add(model=model, item=item)
                #EUR/USD
                item =model(
                    name='EUR/USD',
                    strategy_id=1,
                    symbols='EUR/USD',
                    actions='buy,sell',
                    amount=1,
                    tp_pips=40, 
                    sl_pips=20,
                    params="{'time_start':'09:30:00', 'time_end':'09:30:15', 'change_pip': 10, 'order_pip': 5, 'down': 'buy', 'up': 'sell', 'pending_limit': 120}")
                self.data_orm.add(model=model, item=item)
                #-------------- OneWay
                #XAU/USD
                item = model(
                    name='Buy-XAUUSD', 
                    strategy_id=2,
                    symbols='XAU/USD',
                    actions='buy',
                    amount=1,
                    tp_pips=100,
                    sl_pips=10000,
                    params=""
                )
                self.data_orm.add(model=model, item=item)
                item =model(
                    name='Sell-XAUUSD',
                    strategy_id=2,
                    symbols='XAU/USD',
                    actions='sell',
                    amount=1,
                    tp_pips=100,
                    sl_pips=10000,
                    params=""
                )
                self.data_orm.add(model=model, item=item)
                #EUR/USD
                item =model(
                    name='Buy-EURUSD',
                    strategy_id=2,
                    symbols='EUR/USD',
                    actions='buy',
                    amount=10000,
                    tp_pips=1,
                    sl_pips=1000,
                    params=""
                )
                self.data_orm.add(model=model, item=item)
                item =model(
                    name='Sell-EURUSD',
                    strategy_id=2,
                    symbols='EUR/USD',
                    actions='sell',
                    amount=10000,
                    tp_pips=1,
                    sl_pips=1000,
                    params=""
                )
                self.data_orm.add(model=model, item=item)
                #-------------- Floating
                #XAU/USD
                item =model(
                    name='XAUUSD',
                    strategy_id=3,
                    symbols='XAU/USD',
                    actions='buy,sell',
                    amount=1,
                    tp_pips=300, 
                    sl_pips=100000,
                    params="")
                self.data_orm.add(model=model, item=item)
                #EUR/USD
                item =model(
                    name='EURUSD',
                    strategy_id=3,
                    symbols='EUR/USD',
                    actions='buy,sell',
                    amount=10000,
                    tp_pips=1,
                    sl_pips=100,
                    params=""
                )
                self.data_orm.add(model=model, item=item)
                #-------------- ali_poolback
                #item-1
                item =model(
                    name='EUR/USD',
                    strategy_id=4,
                    symbols='EUR/USD',
                    actions='buy,sell',
                    amount=1,
                    tp_pips=40, 
                    sl_pips=20,
                    params="{'name': 'poolback_4x', 'time_frame': 'm5', 'region': 'UTC', 'time_from': '00:00:00', 'time_to': '21:00:00', 'max_order': 1, 'domain': 10, 'period': {'t1': 9, 'k1': 26, 'sb1': 78, 't2': 36, 'k2': 104, 'sb2': 234}}"
                )
                self.data_orm.add(model=model, item=item)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 7)
            output.message = f"Drop:{drop} | Create:{create} | Truncate:{truncate} | Add:{add}"
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 12)} | {sort(this_method, 35)} | {output.time}", output.message)
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

        try:
            #-------------- Drop
            if drop : self.data_orm.drop(model=model)
            #-------------- Create
            if create : self.data_orm.create(model=model)
            #-------------- Truncate
            if truncate : self.data_orm.truncate(model=model)
            #-------------- Add
            if add:
                self.data_orm.add(model=model, item=model(name="Test-1", strategy_item_id=1, account_id=2, step=1, date_from="2025-01-01 00:00:00", date_to="2025-02-01 23:59:59"))
                self.data_orm.add(model=model, item=model(name="Test-1", strategy_item_id=2, account_id=2, step=1, date_from="2025-01-01 00:00:00", date_to="2025-02-01 23:59:59"))
                self.data_orm.add(model=model, item=model(name="Test-1", strategy_item_id=3, account_id=2, step=1, date_from="2025-01-01 00:00:00", date_to="2025-02-01 23:59:59"))
                self.data_orm.add(model=model, item=model(name="Test-1", strategy_item_id=4, account_id=2, step=1, date_from="2025-01-01 00:00:00", date_to="2025-02-01 23:59:59"))
                self.data_orm.add(model=model, item=model(name="Test-1", strategy_item_id=5, account_id=2, step=1, date_from="2025-01-01 00:00:00", date_to="2025-02-01 23:59:59"))
                self.data_orm.add(model=model, item=model(name="Test-1", strategy_item_id=6, account_id=2, step=1, date_from="2025-01-01 00:00:00", date_to="2025-02-01 23:59:59"))
                self.data_orm.add(model=model, item=model(name="Test-1", strategy_item_id=7, account_id=2, step=1, date_from="2025-01-01 00:00:00", date_to="2025-02-01 23:59:59"))
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 7)
            output.message = f"Drop:{drop} | Create:{create} | Truncate:{truncate} | Add:{add}"
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 12)} | {sort(this_method, 35)} | {output.time}", output.message)
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
    
    #--------------------------------------------- back_execute
    def back_execute(self, drop=False, truncate=False,  create=True, add=True):
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
        model = model_back_execute_db

        try:
            #-------------- Drop
            if drop : self.data_orm.drop(model=model)
            #-------------- Create
            if create : self.data_orm.create(model=model)
            #-------------- Truncate
            if truncate : self.data_orm.truncate(model=model)
            #-------------- Add
            if add:
                #-------------- Dowjones
                self.data_orm.add(model=model, item=model(name="2025", strategy_item_id=1, account_id=1, profit_manager_id=6, money_management_id=1, date_from="2025-01-01 00:00:00", date_to="2026-01-01 00:00:00"))
                self.data_orm.add(model=model, item=model(name="2025-12", strategy_item_id=1, account_id=1, profit_manager_id=6, money_management_id=1, date_from="2025-12-01 00:00:00", date_to="2026-01-01 00:00:00"))
                self.data_orm.add(model=model, item=model(name="2025-11", strategy_item_id=1, account_id=1, profit_manager_id=6, money_management_id=1, date_from="2025-11-01 00:00:00", date_to="2025-12-01 00:00:00"))
                self.data_orm.add(model=model, item=model(name="2025-10", strategy_item_id=1, account_id=1, profit_manager_id=6, money_management_id=1, date_from="2025-10-01 00:00:00", date_to="2025-11-01 00:00:00"))
                self.data_orm.add(model=model, item=model(name="2025-09", strategy_item_id=1, account_id=1, profit_manager_id=6, money_management_id=1, date_from="2025-09-01 00:00:00", date_to="2025-10-01 00:00:00"))
                self.data_orm.add(model=model, item=model(name="2025-08", strategy_item_id=1, account_id=1, profit_manager_id=6, money_management_id=1, date_from="2025-08-01 00:00:00", date_to="2025-09-01 00:00:00"))
                self.data_orm.add(model=model, item=model(name="2025-07", strategy_item_id=1, account_id=1, profit_manager_id=6, money_management_id=1, date_from="2025-07-01 00:00:00", date_to="2025-08-01 00:00:00"))
                self.data_orm.add(model=model, item=model(name="2025-06", strategy_item_id=1, account_id=1, profit_manager_id=6, money_management_id=1, date_from="2025-06-01 00:00:00", date_to="2025-07-01 00:00:00"))
                self.data_orm.add(model=model, item=model(name="2025-05", strategy_item_id=1, account_id=1, profit_manager_id=6, money_management_id=1, date_from="2025-05-01 00:00:00", date_to="2025-06-01 00:00:00"))
                self.data_orm.add(model=model, item=model(name="2025-04", strategy_item_id=1, account_id=1, profit_manager_id=6, money_management_id=1, date_from="2025-04-01 00:00:00", date_to="2025-05-01 00:00:00"))
                self.data_orm.add(model=model, item=model(name="2025-03", strategy_item_id=1, account_id=1, profit_manager_id=6, money_management_id=1, date_from="2025-03-01 00:00:00", date_to="2025-04-01 00:00:00"))
                self.data_orm.add(model=model, item=model(name="2025-02", strategy_item_id=1, account_id=1, profit_manager_id=6, money_management_id=1, date_from="2025-02-01 00:00:00", date_to="2025-03-01 00:00:00"))
                self.data_orm.add(model=model, item=model(name="2025-01", strategy_item_id=1, account_id=1, profit_manager_id=6, money_management_id=1, date_from="2025-01-01 00:00:00", date_to="2025-02-01 00:00:00"))
                #-------------- OneWay
                self.data_orm.add(model=model, item=model(name="Test-1", strategy_item_id=2, account_id=1, profit_manager_id=5, money_management_id=1, date_from="2025-12-01 00:00:00", date_to="2026-01-01 00:00:00"))
                self.data_orm.add(model=model, item=model(name="Test-1", strategy_item_id=3, account_id=1, profit_manager_id=5, money_management_id=1, date_from="2025-12-01 00:00:00", date_to="2026-01-01 00:00:00"))
                self.data_orm.add(model=model, item=model(name="Test-1", strategy_item_id=4, account_id=1, profit_manager_id=5, money_management_id=1, date_from="2025-12-01 00:00:00", date_to="2026-01-01 00:00:00"))
                self.data_orm.add(model=model, item=model(name="Test-1", strategy_item_id=5, account_id=1, profit_manager_id=5, money_management_id=1, date_from="2025-12-01 00:00:00", date_to="2026-01-01 00:00:00"))
                self.data_orm.add(model=model, item=model(name="Test-1", strategy_item_id=6, account_id=1, profit_manager_id=5, money_management_id=1, date_from="2025-12-01 00:00:00", date_to="2026-01-01 00:00:00"))
                self.data_orm.add(model=model, item=model(name="Test-1", strategy_item_id=7, account_id=1, profit_manager_id=5, money_management_id=1, date_from="2025-12-01 00:00:00", date_to="2026-01-01 00:00:00"))
                self.data_orm.add(model=model, item=model(name="Test-1", strategy_item_id=8, account_id=1, profit_manager_id=5, money_management_id=1, date_from="2025-12-01 00:00:00", date_to="2026-01-01 00:00:00"))
                #-------------- ali_poolback
                self.data_orm.add(model=model, item=model(name="2026-02", strategy_item_id=10, account_id=1, profit_manager_id=1, money_management_id=1, date_from="2025-12-01 00:00:00", date_to="2027-01-01 00:00:00"))
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 7)
            output.message = f"Drop:{drop} | Create:{create} | Truncate:{truncate} | Add:{add}"
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 12)} | {sort(this_method, 35)} | {output.time}", output.message)
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

    #--------------------------------------------- profit_manager
    def profit_manager(self, drop=False, truncate=False,  create=True, add=True):
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
        model = model_profit_manager_db

        try:
            #-------------- Drop
            if drop : self.data_orm.drop(model=model)
            #-------------- Create
            if create : self.data_orm.create(model=model)
            #-------------- Truncate
            if truncate : self.data_orm.truncate(model=model)
            #-------------- Add
            if add:
                self.data_orm.add(model=model, item=model(name="0", description="0 to 0"))
                self.data_orm.add(model=model, item=model(name="1", description="1 to 1"))
                self.data_orm.add(model=model, item=model(name="2", description="1 to 2"))
                self.data_orm.add(model=model, item=model(name="3", description="1 to 3"))
                self.data_orm.add(model=model, item=model(name="5", description="1 to 5"))
                self.data_orm.add(model=model, item=model(name="10", description="1 to 10"))
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 7)
            output.message = f"Drop:{drop} | Create:{create} | Truncate:{truncate} | Add:{add}"
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 12)} | {sort(this_method, 35)} | {output.time}", output.message)
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
    
    #--------------------------------------------- profit_manager_item
    def profit_manager_item(self, drop=False, truncate=False,  create=True, add=True):
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
        model = model_profit_manager_item_db

        try:
            #-------------- Drop
            if drop : self.data_orm.drop(model=model)
            #-------------- Create
            if create : self.data_orm.create(model=model)
            #-------------- Truncate
            if truncate : self.data_orm.truncate(model=model)
            #-------------- Add
            if add:
                #---1
                self.data_orm.add(model=model, item=model(profit_manager_id=2, name="1", value=100, tp_value=200, sl_value=-100, at_value=0))
                #---2
                self.data_orm.add(model=model, item=model(profit_manager_id=3, name="1", value=100, tp_value=200, sl_value=-100, at_value=0))
                self.data_orm.add(model=model, item=model(profit_manager_id=3, name="2", value=200, tp_value=300, sl_value=-200, at_value=0))
                #---3
                self.data_orm.add(model=model, item=model(profit_manager_id=4, name="1", value=100, tp_value=200, sl_value=-100, at_value=0))
                self.data_orm.add(model=model, item=model(profit_manager_id=4, name="2", value=200, tp_value=300, sl_value=-200, at_value=0))
                self.data_orm.add(model=model, item=model(profit_manager_id=4, name="3", value=300, tp_value=400, sl_value=-300, at_value=0))
                #---5
                self.data_orm.add(model=model, item=model(profit_manager_id=5, name="1", value=100, tp_value=200, sl_value=-100, at_value=0))
                self.data_orm.add(model=model, item=model(profit_manager_id=5, name="2", value=200, tp_value=300, sl_value=-200, at_value=0))
                self.data_orm.add(model=model, item=model(profit_manager_id=5, name="3", value=300, tp_value=400, sl_value=-300, at_value=0))
                self.data_orm.add(model=model, item=model(profit_manager_id=5, name="4", value=400, tp_value=500, sl_value=-400, at_value=0))
                self.data_orm.add(model=model, item=model(profit_manager_id=5, name="5", value=500, tp_value=600, sl_value=-500, at_value=0))
                #---10
                self.data_orm.add(model=model, item=model(profit_manager_id=6, name="1", value=100, tp_value=100, sl_value=-100, at_value=0))
                self.data_orm.add(model=model, item=model(profit_manager_id=6, name="2", value=200, tp_value=100, sl_value=-100, at_value=0))
                self.data_orm.add(model=model, item=model(profit_manager_id=6, name="3", value=300, tp_value=100, sl_value=-100, at_value=0))
                self.data_orm.add(model=model, item=model(profit_manager_id=6, name="4", value=400, tp_value=100, sl_value=-100, at_value=0))
                self.data_orm.add(model=model, item=model(profit_manager_id=6, name="5", value=500, tp_value=100, sl_value=-100, at_value=0))
                self.data_orm.add(model=model, item=model(profit_manager_id=6, name="6", value=600, tp_value=100, sl_value=-100, at_value=0))
                self.data_orm.add(model=model, item=model(profit_manager_id=6, name="7", value=700, tp_value=100, sl_value=-100, at_value=0))
                self.data_orm.add(model=model, item=model(profit_manager_id=6, name="8", value=800, tp_value=100, sl_value=-100, at_value=0))
                self.data_orm.add(model=model, item=model(profit_manager_id=6, name="9", value=900, tp_value=100, sl_value=-100, at_value=0))
                self.data_orm.add(model=model, item=model(profit_manager_id=6, name="10", value=1000, tp_value=100, sl_value=-100, at_value=0))
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 7)
            output.message = f"Drop:{drop} | Create:{create} | Truncate:{truncate} | Add:{add}"
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 12)} | {sort(this_method, 35)} | {output.time}", output.message)
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

    #--------------------------------------------- money_management
    def money_management(self, drop=False, truncate=False,  create=True, add=True):
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
        model = model_money_management_db

        try:
            #-------------- Drop
            if drop : self.data_orm.drop(model=model)
            #-------------- Create
            if create : self.data_orm.create(model=model)
            #-------------- Truncate
            if truncate : self.data_orm.truncate(model=model)
            #-------------- Add
            if add:
                self.data_orm.add(model=model, item=model(name="0", balance=10000, risk=0, limit_trade=-1, limit_profit=-1, limit_loss=-1, limit_stop=-1,))
                self.data_orm.add(model=model, item=model(name="5", balance=10000, risk=5, limit_trade=-1, limit_profit=-1, limit_loss=-1, limit_stop=-1,))
                self.data_orm.add(model=model, item=model(name="10", balance=10000, risk=10, limit_trade=-1, limit_profit=-1, limit_loss=-1, limit_stop=-1,))
                self.data_orm.add(model=model, item=model(name="15", balance=10000, risk=15, limit_trade=-1, limit_profit=-1, limit_loss=-1, limit_stop=-1,))
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 7)
            output.message = f"Drop:{drop} | Create:{create} | Truncate:{truncate} | Add:{add}"
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 12)} | {sort(this_method, 35)} | {output.time}", output.message)
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
    
    #--------------------------------------------- create_instrument_timeframe_table
    def create_instrument_timeframe_table(self, drop=None, create=None):
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
        tbl_instrument = config["instrument"]["table"]
        timeframes =config["timeframe"]
        defaultSymbols = config["instrument"]["defaultSymbols"]
        
        try:
            #-------------------- Action
            tblList= self.data_orm.items(model=model_instrument_db).data
            for i in tblList:
                for t in timeframes:
                    if i.name in defaultSymbols:
                        tblName =f"{i.name}_{t}"
                        if t =="t1":
                            query = f"""
                                CREATE TABLE IF NOT EXISTS {tblName} (
                                    id SERIAL UNIQUE NOT NULL,
                                    date TIMESTAMP UNIQUE NOT NULL PRIMARY KEY,
                                    bid numeric(6,12),
                                    ask numeric(6,12)                            
                                )"""
                        else:                  
                            query = f"""
                                CREATE TABLE IF NOT EXISTS {tblName} (
                                    id SERIAL UNIQUE NOT NULL,
                                    date TIMESTAMP UNIQUE NOT NULL PRIMARY KEY,
                                    bidopen numeric(6,12),
                                    bidclose numeric(6,12),
                                    bidhigh numeric(6,12),
                                    bidlow numeric(6,12),
                                    askopen numeric(6,12),
                                    askclose numeric(6,12),
                                    askhigh numeric(6,12),
                                    asklow numeric(6,12),
                                    tickqty smallint
                                )"""
                        if drop:
                            output.data["drop"] = self.data_sql.db.execute(f"DROP TABLE IF EXISTS {tblName}")
                            self.log.verbose("rep", f"{sort(self.this_class, 8)} | {sort(this_method, 8)}", f"Drop table {tblName} : {output.status}")
                        if create:
                            output.data["create"] = self.data_sql.db.execute(query)
                            self.log.verbose("rep", f"{sort(self.this_class, 8)} | {sort(this_method, 8)}", f"Create table {tblName} : {output.status}")
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 7)
            output.message = True
            #--------------Verbose
            if verbose : self.log.verbose("rep", f"{sort(self.this_class, 12)} | {sort(this_method, 35)} | {output.time}", output.message)
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