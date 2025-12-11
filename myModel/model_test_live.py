#--------------------------------------------------------------------------------- Location
# models/model_test_live.py

#--------------------------------------------------------------------------------- Description
# model_test_live

#--------------------------------------------------------------------------------- Import
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.inspection import inspect
from sqlalchemy.sql import func
from myLib.database_orm import BaseModel as BaseModel_db
from pydantic import BaseModel as BaseModel_py
from typing import Optional
from datetime import datetime

#--------------------------------------------------------------------------------- Database
class model_test_live_db(BaseModel_db):
    #---Name
    __tablename__ = 'test_live'
    #---Items
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, default=func.now())
    name = Column(String, default='')
    strategy_item_id = Column(Integer, default=0)
    account_id = Column(Integer, default=0)
    status = Column(String, default='')
    description = Column(String, default='')
    enable = Column(Boolean, default=True)
    #---Display
    def __repr__(self) : return f"{self.toDict()}"
    #---Json
    def toDict(self) : return {column.key: getattr(self, column.key) for column in inspect(self).mapper.column_attrs}

#--------------------------------------------------------------------------------- Python
class model_test_live_py(BaseModel_py):
    id : int = 0
    date : datetime = None
    name : str = ''
    strategy_item_id : int = 0
    account_id : int = 0
    status : str = ''
    description : Optional[str] = ''
    enable : bool = True