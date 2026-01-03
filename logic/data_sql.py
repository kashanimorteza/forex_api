#--------------------------------------------------------------------------------- Location
# logic/data_sql.py

#--------------------------------------------------------------------------------- Description
# data_sql

#--------------------------------------------------------------------------------- Import
from logic.startup import config, debug, log_instance
from logic.util import sort, get_tbl_name
from logic.log import Logic_Log
from logic.database_sql import Database_SQL

#--------------------------------------------------------------------------------- Action
class Data_SQL:
    #-------------------------- [Init]
    def __init__(self, database, log=log_instance):
        #--------------------Variable
        self.this_class = self.__class__.__name__
        self.log:Logic_Log = log
        #--------------------Data
        database_cfg = config.get("database", {}).get(database, {})
        #--------------------Instance
        self.db = Database_SQL(
            server=database_cfg.get("server"), 
            host=database_cfg.get("host"), 
            port=database_cfg.get("port"), 
            username=database_cfg.get("username"), 
            password=database_cfg.get("password"), 
            database=database_cfg.get("database"), 
            log=self.log
        )