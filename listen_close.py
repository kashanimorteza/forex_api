#--------------------------------------------------------------------------------- Location
# mylib/listen_close.py

#--------------------------------------------------------------------------------- Description
# listen_close

#--------------------------------------------------------------------------------- Import
import datetime, time
from forexconnect import ForexConnect, fxcorepy
from forexconnect.TableListener import TableListener
import forexconnect.lib

#--------------------------------------------------------------------------------- Class
class CloseTradesListener(TableListener):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        
    def on_added(self, row_id, row):
        item = {"date": datetime.datetime.now().timestamp(), "order_id": row.open_order_id, "trade_id": row.trade_id, "profit": row.gross_pl}
        self.parent.items.append(item)
        #print(f"Trade closed  : {row.open_order_id} | {row.gross_pl} | {row.trade_id} |")

#--------------------------------------------------------------------------------- Class
class Listen_Close:
    #--------------------------------------------- __init__
    def __init__(self, forex_api, items):
        self.forex_api = forex_api
        self.items = items
        self.listener = None
        self.close_table = None
        self.is_running = False
    
    #--------------------------------------------- start
    def start(self):
        print("Listen_Close : Started")
        self.listener = CloseTradesListener(self)
        table_manager = self.forex_api.fx.table_manager
        while table_manager.status != forexconnect.lib.fxcorepy.O2GTableManagerStatus.TABLES_LOADED : time.sleep(0.1)
        self.close_table = table_manager.get_table(ForexConnect.CLOSED_TRADES)
        self.close_table.subscribe_update(fxcorepy.O2GTableUpdateType.INSERT, self.listener)
        self.is_running = True
        try:
            while True : time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping listener...")
            self.stop()
    
    #--------------------------------------------- stop
    def stop(self):
        print("Listen_Close : Stopped")
        if self.close_table and self.listener:
            self.close_table.unsubscribe_update(fxcorepy.O2GTableUpdateType.INSERT, self.listener)
        if self.forex_api:
            self.forex_api.logout()
        self.is_running = False