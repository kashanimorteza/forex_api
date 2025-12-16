#--------------------------------------------------------------------------------- Location
# listen_close.py

#--------------------------------------------------------------------------------- Description
# listen_close

#--------------------------------------------------------------------------------- Import
#--------------------------------------------- Warnings
import re
import logging, warnings, time
warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("root").setLevel(logging.CRITICAL)
#--------------------------------------------- Forex
from forexconnect import ForexConnect, fxcorepy
from forexconnect.TableListener import TableListener
import forexconnect.lib
from myLib.forex import Forex
#--------------------------------------------- Logic
from myLib.logic_global import config, load_forex_api
from myLib.logic_global import debug, log_instance, data_instance, forex_apis
from myLib.logic_management import Logic_Management

#--------------------------------------------------------------------------------- Instance
load_forex_api()
forex_api = forex_apis[1]
forex = Forex(forex_api = forex_api)
logic_management = Logic_Management()

# order_id = '1826945977'
# profit = 100
# logic_management.order_close(order_id=order_id, profit=profit)


#--------------------------------------------------------------------------------- Class
class CloseTradesListener(TableListener):
    def on_added(self, row_id, row):
        order_id = row.open_order_id
        profit = row.gross_pl
        logic_management.order_close(order_id=order_id, profit=profit)

#--------------------------------------------------------------------------------- Action
listener = CloseTradesListener()

table_manager = forex.fx.table_manager
while table_manager.status != forexconnect.lib.fxcorepy.O2GTableManagerStatus.TABLES_LOADED : time.sleep(0.1)

close_table = table_manager.get_table(ForexConnect.CLOSED_TRADES)
close_table.subscribe_update(fxcorepy.O2GTableUpdateType.INSERT, listener)

print("Listening for trade close events... Press Ctrl+C to stop.")
try:
    while True: time.sleep(1)
except KeyboardInterrupt: pass

close_table.unsubscribe_update(fxcorepy.O2GTableUpdateType.INSERT, listener)
forex_api.logout()