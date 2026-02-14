#--------------------------------------------------------------------------------- Location
# implement.py

#--------------------------------------------------------------------------------- Description
# Implement

#--------------------------------------------------------------------------------- Import
from logic.startup import log_instance, data_instance, database_management
from logic.implementation import Logic_Implementation
from logic.data_orm import Data_Orm
from model import *

#--------------------------------------------------------------------------------- Log
log_instance.fileClear()
log_instance.table(drop=True, create=True, add=True)

#--------------------------------------------------------------------------------- Implementation_Management
IM = Logic_Implementation()
IM.create_all_table()
IM.truncate_all_table()
IM.account(drop=True, create=True,truncate=True, add=True)
IM.instrument(drop=True, create=True,truncate=True, add=True)
IM.strategy(drop=True, create=True,truncate=True, add=True)
IM.strategy_item(drop=True, create=True,truncate=True, add=True)
IM.live_execute(drop=False, create=False,truncate=True, add=True)
IM.back_execute(drop=False, create=False,truncate=True, add=True)
IM.profit_manager(drop=False, create=False,truncate=True, add=True)
IM.profit_manager_item(drop=False, create=False,truncate=True, add=True)
IM.money_management(drop=False, create=False,truncate=True, add=True)
#IM.create_instrument_timeframe_table(drop=False, create=True)

db = Data_Orm(database=database_management)
db.truncate(model=model_back_order_db)
db.truncate(model=model_back_order_pending_db)
db.truncate(model=model_back_execute_detaile_db)
db.truncate(model=model_back_profit_manager_detaile_db)
db.truncate(model=model_live_order_db)
db.truncate(model=model_live_execute_detaile_db)