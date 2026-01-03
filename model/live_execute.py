#--------------------------------------------------------------------------------- Location
# model/model_live_execute.py

#--------------------------------------------------------------------------------- Description
# model_live_execute

#--------------------------------------------------------------------------------- Import
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.inspection import inspect
from logic.database_orm import BaseModel as BaseModel_db
from pydantic import BaseModel as BaseModel_py
from typing import Optional
from datetime import datetime

#--------------------------------------------------------------------------------- Database
class model_live_execute_db(BaseModel_db):
    #---Name
    __tablename__ = 'live_execute'
    #---Items
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, default='')
    strategy_item_id = Column(Integer, default=1)
    account_id = Column(Integer, default=1)
    date_from = Column(DateTime, default='2025-01-01 00:00:00')
    date_to = Column(DateTime, default='2030-01-01 00:00:00')
    step = Column(Integer, default=1)
    status = Column(String, default='')
    description = Column(String, default='')
    enable = Column(Boolean, default=True)
    #---Display
    def __repr__(self) : return f"{self.toDict()}"
    #---Json
    def toDict(self):
        data = {column.key: getattr(self, column.key) for column in inspect(self).mapper.column_attrs}
        if data.get('date_from') and isinstance(data['date_from'], datetime) : data['date_from'] = data['date_from'].strftime('%Y-%m-%d %H:%M:%S')
        if data.get('date_to') and isinstance(data['date_to'], datetime) : data['date_to'] = data['date_to'].strftime('%Y-%m-%d %H:%M:%S')
        return data

#--------------------------------------------------------------------------------- Python
class model_live_execute_py(BaseModel_py):
    id : int = 0
    name : str = ''
    strategy_item_id : int = 1
    account_id : int = 1
    date_from : datetime = datetime.strptime('2025-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    date_to : datetime = datetime.strptime('2030-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    step : int = 1
    status : str = ''
    description : Optional[str] = ''
    enable : bool = True