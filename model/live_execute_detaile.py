#--------------------------------------------------------------------------------- Location
# models/model_live_order.py

#--------------------------------------------------------------------------------- Description
# model_live_order

#--------------------------------------------------------------------------------- Import
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.inspection import inspect
from logic.database_orm import BaseModel as BaseModel_db
from pydantic import BaseModel as BaseModel_py
from typing import Optional
from datetime import datetime

#--------------------------------------------------------------------------------- Database
class model_live_execute_detaile_db(BaseModel_db):
    #---Name
    __tablename__ = 'live_execute_detaile'
    #---Items
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime)
    execute_id = Column(Integer, default=0)
    step = Column(Integer, default=0)
    profit_close = Column(Float, default=0)
    profit_open = Column(Float, default=0)
    param = Column(String, default='')
    description = Column(String, default='')
    enable = Column(Boolean, default=True)
    #---Display
    def __repr__(self) : return f"{self.toDict()}"
    #---Json
    def toDict(self):
        data = {column.key: getattr(self, column.key) for column in inspect(self).mapper.column_attrs}
        if data.get('date') and isinstance(data['date'], datetime) : data['date'] = data['date'].strftime('%Y-%m-%d %H:%M:%S')
        return data

#--------------------------------------------------------------------------------- Python
class model_live_execute_detaile_py(BaseModel_py):
    id : int = 0
    date : Optional[str] = ''
    execute_id : int = 0
    step : int = 0
    profit_close : float = 0
    profit_open : float = 0
    param : Optional[str] = ''
    description : Optional[str] = ''
    enable : bool = True