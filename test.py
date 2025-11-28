#--------------------------------------------------------------------------------- Location
# myLib/store.py

#--------------------------------------------------------------------------------- Description
# Store

#--------------------------------------------------------------------------------- Import
import os,sys
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, f"{root_dir}/myLib")
from myLib.forex import Forex
from myLib.forex_api import Forex_Api

#--------------------------------------------------------------------------------- Action
forex_api = Forex_Api(account="acc-history1")
forex_api.login()

forex = Forex(api=forex_api)
ai = forex.account_info()
print(ai)

ai = forex.account_info()
print(ai)



# fx.login()
# open = fx.trade_open(symbol="EUR/USD", action="buy", amount=2000)
# close = fx.trade_close_all()
# fx.logout()
