#--------------------------------------------------------------------------------- Location
# logic/logic_global.py

#--------------------------------------------------------------------------------- Description
# logic_global

#--------------------------------------------------------------------------------- Import
from enum import Enum

#--------------------------------------------------------------------------------- Variable
forex_apis = {}
list_close = []
list_instrument= {}

#--------------------------------------------------------------------------------- Method
#-------------------------- load_config
def load_config():
    import os, yaml
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.environ.get("CONFIG_PATH", os.path.join(root_dir, "config.yaml"))
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

#-------------------------- load_log
def load_log():
    from logic.logic_log import Logic_Log
    return Logic_Log(config=config)

#-------------------------- load_data
def load_data():
    from logic.data_orm import Data_Orm
    from logic.data_sql import Data_SQL
    data_instance = {}
    #---Management
    data_instance['management_orm'] = Data_Orm(database=database_management)
    data_instance['data_orm'] = Data_Orm(database=database_data)
    management_sql = Data_SQL(database=database_management)
    management_sql.db.open()
    data_instance['management_sql'] = management_sql
    #---Data
    data_sql = Data_SQL(database=database_data)
    data_sql.db.open()
    data_instance['data_sql'] = data_sql
    #---Log
    log_sql = Data_SQL(database=database_log)
    log_sql.db.open()
    data_instance['log_sql'] = log_sql

    return data_instance

#-------------------------- load_forex_api
def load_forex_api():
    #---Import
    from model.model_account import model_account_db
    from logic.data_orm import Data_Orm
    from logic.fxcm_api import Fxcm_API
    #---Instance
    db:Data_Orm  = data_instance["management_orm"]
    #---Action
    forex_accounts:list[model_account_db] = db.items(model=model_account_db, enable=True).data
    for account in forex_accounts:
        if account.name !="Back-Test" and account.broker.lower() == "fxcm":
            fxcm_api = Fxcm_API(account_info=account.toDict())
            forex_apis[account.id] = fxcm_api
            #fxcm_api.login()

#-------------------------- load_instrument
def load_instrument():
    from logic.data_orm import Data_Orm
    from model.model_instrument import model_instrument_db
    db:Data_Orm = data_instance["management_orm"]
    result= db.items(model=model_instrument_db, enable=True)
    if result.status : 
        for item in result.data : 
            list_instrument[item.instrument] = item.toDict()

#--------------------------------------------------------------------------------- Enum
#-------------------------- Strategy_Action
class Strategy_Action(str, Enum):
    START = "start"
    STOP = "stop"
    ORDER_CLOSE = "order_close"
    PRICE_CHANGE= "price_change"
    
#-------------------------- Strategy_Run
class Strategy_Run(str, Enum):
    ORDER_OPEN = "order_open"
    ORDER_CLOSE = "order_close"
    ORDER_CLOSE_ALL= "order_close_all"

class Order_Action(str, Enum):
    BUY = "buy"
    SELL = "sell"

#--------------------------------------------------------------------------------- Action
config:dict = load_config()
forexconnect_delay = config.get("forex_connect", {}).get("delay",0)
database_management = config.get("general", {}).get("database_management", {})
database_data = config.get("general", {}).get("database_data", {})
database_log = config.get("general", {}).get("database_log", {})
debug = config.get("debug", {})
log_instance = load_log()
data_instance = load_data()
log_instance.db =data_instance['log_sql']
load_instrument()