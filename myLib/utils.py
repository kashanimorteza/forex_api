#--------------------------------------------------------------------------------- Location
# code/myLib/utils.py

#--------------------------------------------------------------------------------- Description
# Utils

#--------------------------------------------------------------------------------- Import
from __future__ import annotations
import os, yaml
from datetime import timedelta
from myLib.debug import debug

#--------------------------------------------------------------------------------- Action
#-------------------------- load_config
def load_config():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.environ.get("CONFIG_PATH", os.path.join(root_dir, "config.yaml"))
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

#-------------------------- load_config
def load_forex_apis():
    from myLib.data_orm import Data_Orm
    from myModel.model_account import model_account_db
    from myLib.forex_api import Forex_Api

    data_orm = Data_Orm()

    forex_apis = {}
    forex_accounts = data_orm.items(model=model_account_db, enable=True)
    for acc in forex_accounts.data :
        forex_api = Forex_Api(name=acc.name, type=acc.type, username=acc.username, password=acc.password, url=acc.url, key=acc.key)
        forex_api.login()
        forex_apis[acc.id] = forex_api
    return forex_apis

#-------------------------- get_tbl_name
def get_tbl_name(symbol, timeFrame):
    symbol=symbol.replace('/', '')
    symbol=symbol.replace('.', '')
    res = f"{symbol}_{timeFrame}"
    if res[0].isdigit() : res = f'"{res}"'
    return res

#-------------------------- sort
def sort(value, size) : 
    #-------------------- Description
    # IN     : 
    # OUT    : 
    # Action : Sort value 
    return str(value).ljust(size)

#-------------------------- _to_bool
def to_bool(value: str) -> bool:
    #-------------------- Description
    # IN     : 
    # OUT    : 
    # Action : Convert to bool
    if isinstance(value, str):
        v = value.lower()
        if v in {"true", "1", "yes", "y"} : return True
        if v in {"false", "0", "no", "n"} : return False
        raise ValueError(f"Invalid boolean: {value}")
    return bool(value)

#-------------------------- parse_cli_args
def parse_cli_args(argv: list[str]) -> dict[str, object]:
    #-------------------- Description
    # IN     : 
    # OUT    : 
    # Action : Pars cli arguments
    config: dict[str, object] = {}
    for term in argv:
        key, raw_value = term.split("=", 1)
        value = raw_value.strip('"')
        config[key] = value
    return config

#-------------------------- format_dict_block
def format_dict_block(title, data: dict) -> str:
    #-------------------- Description
    # IN     : 
    # OUT    : 
    # Action : Format dictionary to block
    def normalize_value(v):
        if isinstance(v, str):
            if v.lower() in ("true", "false"):
                return v.lower() == "true"
        return v
    data = {k: normalize_value(v) for k, v in data.items()}
    max_key_len = max(len(k) for k in data.keys())
    lines = []
    lines.append(f"{'-' * 46}{title}")
    for key, value in data.items():
        lines.append(f"{key.ljust(max_key_len)} = {value}")
    lines.append("-" * 46)
    return "\n".join(lines)

#--------------------------------------------- timeframe_nex_date
def timeframe_nex_date(timeframe, date):
    #-------------- Description
    # IN     : 
    # OUT    : 
    # Action :
    #-------------- Data
    timeframe = timeframe.lower()
    #--------------Action
    if timeframe == "w1" : date = (date - timedelta(days=7))
    elif timeframe == "d1" : date = (date - timedelta(days=1))
    elif timeframe == "h8": date = (date - timedelta(hours=8))
    elif timeframe == "h6": date = (date - timedelta(hours=6))
    elif timeframe == "h4": date = (date - timedelta(hours=4))
    elif timeframe == "h3": date = (date - timedelta(hours=3))
    elif timeframe == "h2": date = (date - timedelta(hours=4))
    elif timeframe == "h1": date = (date - timedelta(hours=1))
    elif timeframe == "m30": date = (date - timedelta(minutes=30))
    elif timeframe == "m15": date = (date - timedelta(minutes=15))
    elif timeframe == "m5": date = (date - timedelta(minutes=5))
    elif timeframe == "m1": date = (date - timedelta(minutes=1))
    elif timeframe == "t1": date = (date - timedelta(milliseconds=1))
    #--------------Output
    return date

#--------------------------------------------- get_strategy_instance
def get_strategy_instance(strategy, forex, params):
    #-------------- Description
    # IN     : 
    # OUT    : 
    # Action :
    from myStrategy.st_01 import ST_01
    from myStrategy.st_02 import ST_02
    from myStrategy.st_03 import ST_03
    from myStrategy.st_04 import ST_04
    from myStrategy.st_05 import ST_05
    #--------------Action
    if strategy == "st_01" : return ST_01(forex=forex, params=params)
    if strategy == "st_02" : return ST_02(forex=forex, params=params)
    if strategy == "st_03" : return ST_03(forex=forex, params=params)
    if strategy == "st_04" : return ST_04(forex=forex, params=params)
    if strategy == "st_05" : return ST_05(forex=forex, params=params)

#--------------------------------------------------------------------------------- Variable
config = load_config()
forex_apis = load_forex_apis()
database_management = config.get("general", {}).get("database_management", {})
database_data = config.get("general", {}).get("database_data", {})