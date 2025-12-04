#--------------------------------------------------------------------------------- Location
# download.py

#--------------------------------------------------------------------------------- Description
# Download

#--------------------------------------------------------------------------------- Import
import os, sys, shutil
from datetime import datetime

root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, f"{root_dir}/myLib")

from myLib.model import model_output
from myLib.forex import Forex
from myLib.utils import config, parse_cli_args, format_dict_block, to_bool
from myLib.log import Log
from myLib.forex_api import Forex_Api

#--------------------------------------------------------------------------------- Debug
this_class = "Download"
this_method = "Download"

#--------------------------------------------------------------------------------- Variable
output = model_output()

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
clear = args.get("clear") if args.get("clear") not in (None, "") else config['download']['clear']
clear = to_bool(clear)
dedicate = args.get("dedicate") if args.get("dedicate") not in (None, "") else config['download']['dedicate']
dedicate = to_bool(dedicate)
datefrom = args.get("datefrom") if args.get("datefrom") not in (None, "") else config['download']['datefrom']
dateto = args.get("dateto") if args.get("dateto") not in (None, "") else datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
datefrom = datetime.strptime(datefrom, "%Y-%m-%d %H:%M:%S")
dateto = datetime.strptime(dateto, "%Y-%m-%d %H:%M:%S")

#--------------------------------------------------------------------------------- Display
params = {"account": account, "instrument": instrument, "timeframe": timeframe, "mode": mode, "count": count, "repeat": repeat, "delay": delay, "save": save, "bulk": bulk, "datefrom": datefrom, "dateto": dateto}
print(format_dict_block("Download", params))

#------------------------------------------------------------------- [ Action ]
try:
    #--------------instrument
    instruments = config["instrument"]["defaultSymbols"] if instrument == "all" else instrument.split(",")
    #--------------timeframe
    timeframes = config["timeframe"] if timeframe == "all" else timeframe.split(",")
    #--------------params
    if dedicate :
        for timeframe in timeframes:
            for instrument in instruments:
                if clear : 
                    if os.path.exists(f"{root_dir}/History"): shutil.rmtree(f"{root_dir}/History")
                forex_api = Forex_Api(account="acc-trade")
                forex_api.login()
                forex = Forex(forex_api=forex_api)
                forex.account_info()
                forex.db.open()
                forex.store(instrument, timeframe, mode, count, repeat, delay, save, bulk, datefrom, dateto)
                forex.db.close()
                forex_api.logout()
    else :
        forex_api = Forex_Api(account="acc-trade")
        forex_api.login()
        forex = Forex(forex_api=forex_api)
        forex.account_info()
        forex.db.open()
        for timeframe in timeframes:
            for instrument in instruments:
                if clear : 
                    if os.path.exists(f"{root_dir}/History"): shutil.rmtree(f"{root_dir}/History")
                forex.store(instrument, timeframe, mode, count, repeat, delay, save, bulk, datefrom, dateto)        
        forex.db.close()
        forex_api.logout()
except Exception as e:
    #--------------Error
    output.status = False
    output.message = {"class":this_class, "method":this_method, "error": str(e)}
    print(output)
