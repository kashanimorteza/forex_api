#--------------------------------------------------------------------------------- Location
# logic/logic_util.py

#--------------------------------------------------------------------------------- Description
# Logic Util

#--------------------------------------------------------------------------------- Import
from __future__ import annotations
from pydantic import BaseModel
from typing import Any

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