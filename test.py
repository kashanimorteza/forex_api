#--------------------------------------------------------------------------------- Location
# myLib/store.py

#--------------------------------------------------------------------------------- Description
# Store

#--------------------------------------------------------------------------------- Import
import os,sys, ast
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, f"{root_dir}/myLib")
sys.path.insert(0, f"{root_dir}/myModel")
sys.path.insert(0, f"{root_dir}/myStrategy")
from myLib.database_orm import database_orm
from myLib.data_orm import data_orm
from myLib.forex import Forex
from myLib.listener import Listener
from myLib.forex_api import Forex_Api
from myModel import *
from myStrategy import *

data = data_orm()

# #--------------------------------------------------------------------------------- Action
# forex = Forex(account="acc-trade")
# forex.api.login()
# result = forex.account_info()
# print(result)
# forex.api.logout()

#--------------------------------------------------------------------------------- Database_orm
# db = database_orm()
# db.create_tables()

# obj = strategy_model_db(name="ST01", description="ST01", enable=True)
# data.add(model=strategy_model_db, item=obj)

# params = {
#     "symbol": "EUR/USD",
#     "amount": 10000,
#     "tp_pips": 1,
#     "st_pips": 10,
# }
# obj = strategy_item_model_db(strategy_id=1, name="ST01-EURUSD", description="ST01-EURUSD", enable=True, params=str(params))
# data.add(model=strategy_item_model_db, item=obj)

#--------------------------------------------------------------------------------- Listener
# forex_api = Forex_Api(account="acc-trade")
# forex_api.login()

# forex = Forex(forex_api = forex_api)
# forex.account_info()

# obj = Listener(forex=forex)
# obj.read_trade()

#--------------------------------------------------------------------------------- Action
forex_api = Forex_Api(account="acc-trade")
forex_api.login()
forex = Forex(forex_api = forex_api)
forex.account_info()

obj = data.item(model=strategy_item_model_db, id=1)
params = ast.literal_eval(obj.data[0].params)
st = ST01(forex=forex, params=params)
st.start()

forex.api.logout()

# #--------------------------------------------------------------------------------- Action
# forex = Forex(account="acc-history1")
# datefrom = '2020-01-01 00:00:00'
# dateto = '2020-12-31 23:59:59'
# datefrom = datetime.strptime(datefrom, "%Y-%m-%d %H:%M:%S")
# dateto = datetime.strptime(dateto, "%Y-%m-%d %H:%M:%S")
# result = forex.store("EUR/USD", "W1", "complete", 1000, 1, 0, False, False, datefrom, dateto)
# print(result)
