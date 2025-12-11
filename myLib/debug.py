debug = {
    "Implementation" : 
    {
        "instrument":{"log":False, "verbose":True, "model":"Implementation"},
        "account":{"log":False, "verbose":True, "model":"Implementation"},
        "create_symbol_table":{"log":False, "verbose":False, "model":"Implementation"},
        "set_symbol_category":{"log":False, "verbose":False, "model":"Implementation"},
        "create_symbol_timeframe_table":{"log":False, "verbose":False, "model":"Implementation"}
    },
    "Forex_Api" : 
    {
        "login":{"log":False, "verbose":True, "model":"Forex"},
        "logout":{"log":False, "verbose":True, "model":"Forex"},
    },
    "Forex" : 
    {
        "store":{"log":False, "verbose":True, "model":"Forex"},
        "symbol":{"log":False, "verbose":True, "model":"Forex"},
        "history":{"log":False, "verbose":True, "model":"Forex"},
        "account_info":{"log":False, "verbose":True, "model":"Forex"},
        "trade_list":{"log":False, "verbose":True, "model":"Forex"},
        "trade_open":{"log":False, "verbose":True, "model":"Forex"},
        "trade_close":{"log":False, "verbose":True, "model":"Forex"},
        "trade_close_all":{"log":False, "verbose":True, "model":"Forex"},
    },
    "Data" : 
    {
        "save":{"log":False, "verbose":True, "model":"Data"},
        "get_max_min":{"log":False, "verbose":False, "model":"Data"},
    },
    "Database_Orm" : 
    {
        "drop":{"log":False, "verbose":False, "model":"Database_Orm"},
        "create":{"log":False, "verbose":False, "model":"Database_Orm"},
        "truncate":{"log":False, "verbose":False, "model":"Database_Orm"},
    },
    "ST01" : 
    {
        "start":{"log":False, "verbose":True, "model":"Data"},
        "next":{"log":False, "verbose":False, "model":"Data"},
        "close":{"log":False, "verbose":False, "model":"Data"}
    },
}