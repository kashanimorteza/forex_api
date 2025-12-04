#--------------------------------------------------------------------------------- Location
# listen_close.py

#--------------------------------------------------------------------------------- Description
# listen_close

#--------------------------------------------------------------------------------- Import
#--------------------------------------------- Warnings
import logging, warnings
warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("root").setLevel(logging.CRITICAL)
#--------------------------------------------- General
import os, sys, time, ast, threading
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, f"{root_dir}/myLib")
sys.path.insert(0, f"{root_dir}/myModel")
sys.path.insert(0, f"{root_dir}/myStrategy")
#--------------------------------------------- Forex
from forexconnect import ForexConnect, fxcorepy
from forexconnect.TableListener import TableListener
import forexconnect.lib
#--------------------------------------------- Me
from myLib.log import Log
from myLib.forex_api import Forex_Api
from myLib.forex import Forex
from myLib.data_orm import Data_Orm
from myModel import *
from myStrategy import *

#--------------------------------------------------------------------------------- Instance
log = Log()
data_orm = Data_Orm()
forex_api = Forex_Api(account="acc-trade")
forex = Forex(forex_api = forex_api)
forex_api.login()
forex.account_info()

#--------------------------------------------------------------------------------- Class
class CloseTradesListener(TableListener):
    def on_added(self, row_id, row):
        order_id = row.open_order_id
        action = row.buy_sell
        profit = row.gross_pl

        strategy_item_id = data_orm.items(model=model_strategy_item_trade_db, order_id=order_id).data[0].strategy_item_id
        strategy_id = data_orm.items(model=model_strategy_item_db, id=strategy_item_id).data[0].strategy_id
        params = data_orm.items(model=model_strategy_item_db, id=strategy_item_id).data[0].params
        params = ast.literal_eval(params)
        params["item_id"] = strategy_item_id

        if strategy_id == 1:
            strategy = Strategy_01(forex=forex, params=params)
        if strategy_id == 2:
            strategy = Strategy_02(forex=forex, params=params)
        
        log.verbose("rep", f"Listen | {action}", profit)

        t = threading.Thread(target=strategy.next, args=({"order_id": order_id, "action": action, "profit": profit},))
        t.start()

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