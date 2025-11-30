#--------------------------------------------------------------------------------- Location
# myLib/store.py

#--------------------------------------------------------------------------------- Description
# Store

#--------------------------------------------------------------------------------- Import
import os,sys
from datetime import datetime
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, f"{root_dir}/myLib")
from myLib.forex import Forex
from myLib.forex_api import Forex_Api

# #--------------------------------------------------------------------------------- Action
# forex = Forex(account="acc-history1")
# forex.api.login()
# result = forex.account_info()
# print(result)
# forex.api.logout()

#--------------------------------------------------------------------------------- Action
forex = Forex(account="acc-history1")
datefrom = '2020-01-01 00:00:00'
dateto = '2020-12-31 23:59:59'
datefrom = datetime.strptime(datefrom, "%Y-%m-%d %H:%M:%S")
dateto = datetime.strptime(dateto, "%Y-%m-%d %H:%M:%S")
result = forex.store("EUR/USD", "W1", "complete", 1000, 1, 0, False, False, datefrom, dateto)
print(result)
