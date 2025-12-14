#--------------------------------------------------------------------------------- Location
# myLib/test.py

#--------------------------------------------------------------------------------- Description
# test

#--------------------------------------------------------------------------------- Import
from myLib.logic_global import load_forex_api, load_data
from myLib.logic_management import Logic_Management

#--------------------------------------------------------------------------------- Action  : Order cloese
load_forex_api()
lm = Logic_Management()
order_id = '1826677525'
lm.order_close(order_id=order_id)
order_detail = lm.order_detaile(order_id='1826677525').data
strategy = lm.get_strategy(order_detail=order_detail).data
result = strategy.order_close(order_detail=order_detail)

