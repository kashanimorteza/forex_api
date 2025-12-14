#--------------------------------------------------------------------------------- Location
# myLib/data_sql.py

#--------------------------------------------------------------------------------- Description
# data_sql

#--------------------------------------------------------------------------------- Import
import inspect, time
from myLib.model import model_output
from myLib.logic_global import config, debug, log_instance
from myLib.utils import sort, get_tbl_name
from myLib.log import Log
from myLib.database_sql import Database_SQL

#--------------------------------------------------------------------------------- Action
class Data_SQL:
    #-------------------------- [Init]
    def __init__(self, database, log=log_instance):
        #--------------------Variable
        self.this_class = self.__class__.__name__
        self.log:Log = log
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