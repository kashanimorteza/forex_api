#--------------------------------------------------------------------------------- Location
# download.py

#--------------------------------------------------------------------------------- Description
# Download

#--------------------------------------------------------------------------------- Import
import sys
from datetime import datetime
from myLib.model import model_output
from myLib.logic_global import config
from myLib.utils import parse_cli_args, format_dict_block, to_bool
from myLib.fxcm_api import Forex
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
dateto = args.get("dateto") if args.get("dateto") not in (None, "") else config['download']['dateto']
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
                account_cfg = config.get("forex_connect", {}).get(account, {})
                forex_api = Forex_Api(
                    name=account, 
                    type=account_cfg.get("type"), 
                    username=account_cfg.get("username"), 
                    password=account_cfg.get("password"), 
                    url=account_cfg.get("url"), 
                    key=account_cfg.get("key")
                )
                forex_api.login()
                forex = Forex(forex_api=forex_api)
                forex.store(instrument, timeframe, mode, count, repeat, delay, save, bulk, datefrom, dateto)
                forex_api.logout()
    else :
        account_cfg = config.get("forex_connect", {}).get(account, {})
        forex_api = Forex_Api(
            name=account, 
            type=account_cfg.get("type"), 
            username=account_cfg.get("username"), 
            password=account_cfg.get("password"), 
            url=account_cfg.get("url"), 
            key=account_cfg.get("key")
        )
        forex_api.login()
        forex = Forex(forex_api=forex_api)
        for timeframe in timeframes:
            for instrument in instruments:
                forex.store(instrument, timeframe, mode, count, repeat, delay, save, bulk, datefrom, dateto)        
        forex_api.logout()
except Exception as e:
    #--------------Error
    output.status = False
    output.message = {"class":this_class, "method":this_method, "error": str(e)}
    print(output)


#if clear : if os.path.exists(f"{root_dir}/History"): shutil.rmtree(f"{root_dir}/History")
