#--------------------------------------------------------------------------------- Location
# implement.py

#--------------------------------------------------------------------------------- Description
# Implement

#--------------------------------------------------------------------------------- Import
from myLib.logic_global import log_instance
from myLib.implementation import Implementation

#--------------------------------------------------------------------------------- Log
log_instance.fileClear()
log_instance.table(drop=True, create=True, add=True)

#--------------------------------------------------------------------------------- Implementation_Management
IM = Implementation()
IM.create_all_table()
IM.truncate_all_table()
IM.account(drop=True, create=True,truncate=True, add=True)
IM.instrument(drop=True, create=True,truncate=True, add=True)
IM.strategy(drop=True, create=True,truncate=True, add=True)
IM.strategy_item(drop=True, create=True,truncate=True, add=True)
IM.live_execute(drop=True, create=True,truncate=True, add=True)
IM.live_order(drop=True, create=True, truncate=True, add=True)
IM.back_execute(drop=True, create=True,truncate=True, add=True)
IM.back_order(drop=True, create=True, truncate=True, add=True)
#IM.create_instrument_timeframe_table(drop=False, create=False)