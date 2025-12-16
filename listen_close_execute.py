#--------------------------------------------------------------------------------- Location
# mylib/listen_close_execute.py

#--------------------------------------------------------------------------------- Description
# listen_close_execute

#--------------------------------------------------------------------------------- Import
import time
from myLib.logic_management import Logic_Management 

#--------------------------------------------------------------------------------- Class
class Listen_Close_Execute:
     #--------------------------------------------- init
    def __init__(self, items, sleep_time=1):
        self.items = items
        self.sleep_time = sleep_time
        self.logic_management = Logic_Management()
    
    #--------------------------------------------- start
    def start(self):
        while True:
            for item in self.items:
                print(f"Listen_Close_Execute : Start :  {item}")
                order_id = item.get("order_id")
                profit = item.get("profit")
                self.logic_management.order_close(order_id=order_id, profit=profit)
                print(f"Listen_Close_Execute : End :  {item}")
                self.items.remove(item)
            time.sleep(self.sleep_time )