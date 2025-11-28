#--------------------------------------------------------------------------------- Location
# myLib/store.py

#--------------------------------------------------------------------------------- Description
# Store

#--------------------------------------------------------------------------------- Import
import os, sys, time, shutil
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, f"{root_dir}/myLib")
from datetime import datetime
from myLib.model import model_output
from myLib.forex import Forex
from myLib.store import Store
from myLib.data import Data
from myLib.database import Database
from myLib.forex_api import Forex_Api
from myLib.utils import config, debug, sort, parse_cli_args, format_dict_block, timeframe_nex_date, to_bool
from myLib.log import Log

#--------------------------------------------------------------------------------- Debug
this_class = "Download"
this_method = "Download"

#--------------------------------------------------------------------------------- Variable
output = model_output()
db = Database.instance()
data = Data(log=Log(), db=db)
params = []
processes = {}

#--------------------------------------------------------------------------------- Args
args = parse_cli_args(sys.argv[1:])
account = args.get("account") if args.get("account") not in (None, "") else config['forex_connect']['default']
instrument = args.get("instrument") if args.get("instrument") not in (None, "") else config['download']['instrument']
timeframe = args.get("timeframe") if args.get("timeframe") not in (None, "") else config['download']['timeframe']
mode = args.get("mode") if args.get("mode") not in (None, "") else config['download']['mode']
count = args.get("count") if args.get("count") not in (None, "") else config['download']['count']
count = int(count)
repeat = args.get("repeat") if args.get("repeat") not in (None, "") else config['download']['repeat']
repeat = int(repeat)
delay = args.get("delay") if args.get("delay") not in (None, "") else config['download']['delay']
delay = int(delay)
bulk = args.get("bulk") if args.get("bulk") not in (None, "") else config['download']['bulk']
bulk = to_bool(bulk)
save = args.get("save") if args.get("save") not in (None, "") else config['download']['save']
save = to_bool(save)
datefrom = args.get("datefrom") if args.get("datefrom") not in (None, "") else config['download']['datefrom']
dateto = args.get("dateto") if args.get("dateto") not in (None, "") else datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
datefrom = datetime.strptime(datefrom, "%Y-%m-%d %H:%M:%S")
dateto = datetime.strptime(dateto, "%Y-%m-%d %H:%M:%S")

#--------------------------------------------------------------------------------- Display
params = { "account": account, "instrument": instrument, "timeframe": timeframe, "mode": mode, "count": count, "repeat": repeat, "delay": delay, "save": save, "bulk": bulk, "datefrom": datefrom, "dateto": dateto}
print(format_dict_block("Download", params))

#------------------------------------------------------------------- [ Action ]
try:
    #--------------instrument
    instruments = config["instrument"]["defaultSymbols"] if instrument == "all" else instrument.split(",")
    #--------------timeframe
    timeframes = config["timeframe"] if timeframe == "all" else timeframe.split(",")
    #--------------params
    for timeframe in timeframes:
        for instrument in instruments:
            if os.path.exists(f"{root_dir}/History"): shutil.rmtree(f"{root_dir}/History")

            forex_api = Forex_Api(account="acc-history1")
            forex_api.login()
            forex = Forex(api=forex_api)
            store = Store(data=data, forex=forex)
            db.open()

            datefrom = args.get("datefrom") if args.get("datefrom") not in (None, "") else config['download']['datefrom']
            dateto = args.get("dateto") if args.get("dateto") not in (None, "") else datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            datefrom = datetime.strptime(datefrom, "%Y-%m-%d %H:%M:%S")
            dateto = datetime.strptime(dateto, "%Y-%m-%d %H:%M:%S")
            if mode == "up":
                d = data.get_max_min(instrument=instrument, timeframe=timeframe, mode="max", filed="Date")
                if d.status and d.data: 
                    datefrom = d.data
                    datefrom = timeframe_nex_date(mode=mode, date=datefrom, timeframe=timeframe)
            elif mode == "down":
                d = data.get_max_min(instrument=instrument, timeframe=timeframe, mode="min", filed="Date")
                if d.status and d.data : 
                    dateto = d.data
                    dateto = timeframe_nex_date(mode=mode,date=dateto, timeframe=timeframe)

            store.run(instrument, timeframe, mode, count, repeat, delay, save, bulk, datefrom, dateto)

            forex_api.logout()
            db.close()
except Exception as e:
    #--------------Error
    output.status = False
    output.message = {"class":this_class, "method":this_method, "error": str(e)}
