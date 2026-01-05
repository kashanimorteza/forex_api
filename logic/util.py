#--------------------------------------------------------------------------------- Location
# logic/logic_util.py

#--------------------------------------------------------------------------------- Description
# Logic Util

#--------------------------------------------------------------------------------- Import
from __future__ import annotations
from pydantic import BaseModel
from typing import Any
import pytz

#--------------------------------------------------------------------------------- Class
class model_output(BaseModel):
    class_name : str = ''
    method_name : str = ''
    status : bool = True
    time : int = 0
    data : Any = {}
    message : Any = {}

#--------------------------------------------------------------------------------- Action
#---------------------------------------------get_tbl_name
def get_tbl_name(symbol, timeFrame):
    #-------------------- Description
    # IN     : 
    # OUT    : 
    # Action :
    #-------------------- Action
    symbol=symbol.replace('/', '')
    symbol=symbol.replace('.', '')
    res = f"{symbol}_{timeFrame}".lower()
    if res[0].isdigit() : res = f'"{res}"'
    return res

#---------------------------------------------sort
def sort(value, size) : 
    #-------------------- Description
    # IN     : 
    # OUT    : 
    # Action :
    #-------------------- Action
    return str(value).ljust(size)

#---------------------------------------------to_bool
def to_bool(value: str) -> bool:
    #-------------------- Description
    # IN     : 
    # OUT    : 
    # Action :
    #-------------------- Action
    if isinstance(value, str):
        v = value.lower()
        if v in {"true", "1", "yes", "y"} : return True
        if v in {"false", "0", "no", "n"} : return False
        raise ValueError(f"Invalid boolean: {value}")
    return bool(value)

#---------------------------------------------parse_cli_args
def parse_cli_args(argv: list[str]) -> dict[str, object]:
    #-------------------- Description
    # IN     : 
    # OUT    : 
    # Action :
    #-------------------- Action
    config: dict[str, object] = {}
    for term in argv:
        key, raw_value = term.split("=", 1)
        value = raw_value.strip('"')
        config[key] = value
    return config

#---------------------------------------------format_dict_block
def format_dict_block(title, data: dict) -> str:
    #-------------------- Description
    # IN     : 
    # OUT    : 
    # Action :
    #-------------------- Action
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

#--------------------------------------------- time_change_utc_newyork
def time_change_utc_newyork(date):
    #--------------Action
    utc = pytz.utc
    ny = pytz.timezone("America/New_York")
    utc_dt = utc.localize(date)
    output = utc_dt.astimezone(ny)
    #--------------Return
    return output

#--------------------------------------------- price_pips
def cal_price_pips(price, pips, digits, point_size)-> float:
    #--------------Action
    output = round(price + pips * point_size, digits)
    #--------------Return
    return output

#--------------------------------------------- cal_size
def cal_size(balance, price, pips, risk, digits, point_size)-> float:
    #--------------Action
    pip_value = cal_price_pips(price, pips, digits, point_size) -price
    risk_value = balance * (risk / 100)
    size = risk_value/pip_value
    #--------------Return
    return size

#--------------------------------------------- cal_tp_sl
def cal_tp_sl(action, ask, bid, tp_pips, sl_pips, digits, point_size)-> model_output:
    spred =float(f"{abs(ask-bid):.{digits}f}")
    if action == "buy":
        price_open = ask
        tp = cal_price_pips(bid, (tp_pips + spred), digits, point_size)
        sl = cal_price_pips(bid, -(sl_pips - spred), digits, point_size)
    elif action == "sell":
        price_open = bid
        tp = cal_price_pips(ask, -(tp_pips + spred), digits, point_size)
        sl = cal_price_pips(ask, (sl_pips - spred), digits, point_size)
    return price_open, tp, sl, spred

#--------------------------------------------- cal_movement
def cal_movement(action, price, ask, bid, digits, point_size)-> model_output:
    #--------------Action
    output = (bid - price) if action == "buy" else (price - ask)
    output = float(f"{output:.{digits}f}")
    #--------------Return
    return output

#--------------------------------------------- cal_percent_of_value
def cal_percent_of_value(value_1, value_2)-> int:
    return (value_2 / value_1) * 100

#--------------------------------------------- cal_value_of_percent
def cal_value_of_percent(value_1, value_2, digits, point_size )-> int:
    return float(f"{((value_1 * value_2) / 100):.{digits}f}")

#--------------------------------------------- cal_profit
def cal_profit(action, amount, price_open, ask, bid, digits, point_size)-> model_output:
    #--------------Action
    if action == "buy" :
        price_close = bid 
        profit = (bid - price_open) * amount
    if action == "sell" : 
        price_close = ask
        profit = (price_open - ask) * amount
    profit = float(f"{profit:.{2}f}")
    #--------------Return
    return profit, price_close