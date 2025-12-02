#--------------------------------------------------------------------------------- Location
# myLib/store.py

#--------------------------------------------------------------------------------- Description
# Store

#--------------------------------------------------------------------------------- Import
import os,sys
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, f"{root_dir}/myLib")
sys.path.insert(0, f"{root_dir}/strategy")
from myLib.forex import Forex
from strategy.st01 import ST01

# #--------------------------------------------------------------------------------- Action
# forex = Forex(account="acc-trade")
# forex.api.login()
# result = forex.account_info()
# print(result)
# forex.api.logout()

#--------------------------------------------------------------------------------- Action
forex = Forex(account="acc-trade")
forex.api.login()
forex.account_info()


st = ST01(forex=forex, symbol="EUR/USD", amount=10000, tp_pips=1, st_pips=5)
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
