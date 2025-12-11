#--------------------------------------------------------------------------------- Location
# implement.py

#--------------------------------------------------------------------------------- Description
# Implement

#--------------------------------------------------------------------------------- Import
import os, sys
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, f"{root_dir}/myLib")
from myLib.log import Log
from myLib.implementation import Implementation_Management

#--------------------------------------------------------------------------------- Log
log = Log()
log.fileClear()
log.table(drop=True, create=True, add=True)

#--------------------------------------------------------------------------------- Implementation_Management
IM = Implementation_Management()
IM.tables()
IM.instrument(drop=True, create=True,truncate=True, add=True)
IM.account(drop=True, create=True,truncate=True, add=True)
IM.strategy(drop=True, create=True,truncate=True, add=True)
IM.strategy_item(drop=True, create=True,truncate=True, add=True)
IM.test_live(drop=True, create=True,truncate=True, add=True)