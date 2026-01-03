#--------------------------------------------------------------------------------- Location
# mylib/listen_close_execute.py

#--------------------------------------------------------------------------------- Description
# listen_close_execute

#--------------------------------------------------------------------------------- Import
import time
from logic.live import Logic_Live 

#--------------------------------------------------------------------------------- Class
class Listen_Close_Execute:
     #--------------------------------------------- init
    def __init__(self, items, sleep_time=1):
        self.items = items
        self.sleep_time = sleep_time
        self.logic = Logic_Live()
    
    #--------------------------------------------- start
    def start(self):
        while True:
            for item in self.items:
                #print(f"Trade Execute : {item['order_id']} | {item['profit']} | {item['trade_id']} |")
                date_close = item.get("date_close")
                order_id = item.get("order_id")
                trade_id = item.get("trade_id")
                profit = item.get("profit")
                price_close = item.get("price_close")
                self.logic.order_closed(order_id=order_id, trade_id=trade_id, profit=profit, date_close=date_close, price_close=price_close)
                self.items.remove(item)
            time.sleep(self.sleep_time )