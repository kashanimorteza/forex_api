#--------------------------------------------------------------------------------- Location
# myLib/test.py

#--------------------------------------------------------------------------------- Description
# test

#--------------------------------------------------------------------------------- Import
from myLib.logic_global import load_forex_api
from myLib.logic_management import Logic_Management
from myLib.fxcm_api import Forex
from forexconnect import ForexConnect, fxcorepy
load_forex_api()
from myLib.logic_global import forex_apis

#--------------------------------------------------------------------------------- Action  : Order cloese
def run() :
    command = fxcorepy.Constants.Commands.CREATE_ORDER
    order_type = fxcorepy.Constants.Orders.TRUE_MARKET_OPEN
    fx = forex_apis[1]
    
    # Create and send request
    request = fx.fx.create_order_request(
        ACCOUNT_ID=fx.id,
        command=command, 
        order_type=order_type,
        BUY_SELL= "B",
        SYMBOL = "EUR/USD",
        AMOUNT= 1000
    )
    
    # Send synchronous request - waits for response
    response = fx.fx.send_request(request)
    
    # Get order_id directly from response
    order_id = getattr(response, "order_id", None) if response else None
    
    if order_id:
        print(f"Order ID: {order_id}")
    else:
        print("Failed to get order ID from response")
    
    return order_id

run()

