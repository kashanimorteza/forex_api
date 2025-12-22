#--------------------------------------------------------------------------------- Location
# models/model_back_execute.py

#--------------------------------------------------------------------------------- Description
# model_back_execute

#--------------------------------------------------------------------------------- Import
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.inspection import inspect
from sqlalchemy.sql import func
from myLib.database_orm import BaseModel as BaseModel_db
from pydantic import BaseModel as BaseModel_py
from typing import Optional

#--------------------------------------------------------------------------------- Database
class model_back_execute_db(BaseModel_db):
    #---Name
    __tablename__ = 'back_execute'
    #---Items
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, default='')
    strategy_item_id = Column(Integer, default=0)
    account_id = Column(Integer, default=0)
    date_from = Column(DateTime, default=func.now(), server_default=func.now())
    date_to = Column(DateTime, default=func.now(), server_default=func.now())
    status = Column(String, default='')
    count = Column(Integer, default=1)
    description = Column(String, default='')
    enable = Column(Boolean, default=True)
    #---Display
    def __repr__(self) : return f"{self.toDict()}"
    #---Json
    def toDict(self) : return {column.key: getattr(self, column.key) for column in inspect(self).mapper.column_attrs}

#--------------------------------------------------------------------------------- Python
class model_back_execute_py(BaseModel_py):
    id : int = 0
    name : str = ''
    date_from : Optional[str] = ''
    date_to : Optional[str] = ''
    account_id : int = 0
    status : str = ''
    count : int = 1
    description : Optional[str] = ''
    enable : bool = True