#--------------------------------------------------------------------------------- Location
# implement.py

#--------------------------------------------------------------------------------- Description
# Implement

#--------------------------------------------------------------------------------- Import
from myLib.log import Log
from myLib.implementation import Implementation_Management

#--------------------------------------------------------------------------------- Log
log = Log()
log.fileClear()
log.table(drop=True, create=True, add=True)

#--------------------------------------------------------------------------------- Implementation_Management
IM = Implementation_Management()
IM.create_all_table()
IM.truncate_all_table()
IM.instrument(drop=True, create=True,truncate=True, add=True)
IM.account(drop=True, create=True,truncate=True, add=True)
IM.strategy(drop=True, create=True,truncate=True, add=True)
IM.strategy_item(drop=True, create=True,truncate=True, add=True)
IM.live_execute(drop=True, create=True,truncate=True, add=True)