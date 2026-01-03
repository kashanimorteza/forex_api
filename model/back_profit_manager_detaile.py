#--------------------------------------------------------------------------------- Location
# models/model_back_profit_manager_detaile.py

#--------------------------------------------------------------------------------- Description
# model_back_profit_manager_detaile

#--------------------------------------------------------------------------------- Import
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.inspection import inspect
from logic.database_orm import BaseModel as BaseModel_db
from pydantic import BaseModel as BaseModel_py
from typing import Optional
from datetime import datetime

#--------------------------------------------------------------------------------- Database
class model_back_profit_manager_detaile_db(BaseModel_db):
    #---Name
    __tablename__ = 'back_profit_manager_detaile'
    #---Items
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime)
    order_id = Column(Integer, default=0)
    ask = Column(Float, default=0)
    bid = Column(Float, default=0)
    execute = Column(String, default='')
    value = Column(Float, default=0)
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
class model_back_profit_manager_detaile_py(BaseModel_py):
    id : int = 0
    date : Optional[str] = ''
    order_id : int = 0
    ask : float = 0
    bid : float = 0
    execute : Optional[str] = ''
    value : float = 0
    description : Optional[str] = ''
    enable : bool = True