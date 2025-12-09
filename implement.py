#--------------------------------------------------------------------------------- Location
# implement.py

#--------------------------------------------------------------------------------- Description
# Implement

#--------------------------------------------------------------------------------- Import
import os,sys, time
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, f"{root_dir}/myLib")
from myLib.log import Log
from myLib.database import Database
from myLib.implementation import Implementation
from myLib.database_orm import Database_Orm

#--------------------------------------------------------------------------------- Variable
start_time = time.time()

#--------------------------------------------------------------------------------- Log
db = Database_Orm()
db.create_tables()

#--------------------------------------------------------------------------------- Log
log = Log()
log.fileClear()
log.table(drop=True, create=True, add=True)

#--------------------------------------------------------------------------------- Implementation
db = Database.instance()
db.open(name="Implement")
impelment = Implementation(db=db)

#-------------------- Instrument
impelment.instrument(drop=True, create=True,truncate=True, add=True)

# lst = ["EUR/USD", "EUR/GBP", "EUR/CHF", "EUR/JPY", "EUR/AUD", "EUR/CAD", "EUR/NZD"]
# for n in lst: impelment.set_instrument_category(n, 1)
# lst = ["GBP/USD","GBP/JPY", "GBP/CHF", "GBP/NZD", "GBP/AUD", "GBP/CAD"]
# for n in lst: impelment.set_instrument_category(n, 2)
# lst = ["AUD/USD", "AUD/CAD", "AUD/JPY", "AUD/NZD", "AUD/CHF"]
# for n in lst: impelment.set_instrument_category(n, 3)
# lst = ["NZD/USD", "NZD/JPY", "NZD/CHF", "NZD/CAD"]
# for n in lst: impelment.set_instrument_category(n, 4)
# lst = ["USD/JPY", "USD/CHF", "USD/CAD"]
# for n in lst: impelment.set_instrument_category(n, 5)
# lst = ["CAD/JPY", "CAD/CHF"]
# for n in lst: impelment.set_instrument_category(n, 6)
# lst = ["CHF/JPY"]
# for n in lst: impelment.set_instrument_category(n, 7)
# lst = ["XAU/USD", "XAG/USD"]
# for n in lst: impelment.set_instrument_category(n, 8)
# lst = ["USOil", "UKOil"]
# for n in lst: impelment.set_instrument_category(n, 9)
# table = impelment.create_instrument_timeframe_table(drop=True, create=True)
# db.close(name="Implement")