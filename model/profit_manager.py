#--------------------------------------------------------------------------------- Location
# models/model_profit_manager.py

#--------------------------------------------------------------------------------- Description
# model_profit_manager

#--------------------------------------------------------------------------------- Import
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.inspection import inspect
from logic.database_orm import BaseModel as BaseModel_db
from pydantic import BaseModel as BaseModel_py
from typing import Optional

#--------------------------------------------------------------------------------- Database
class model_profit_manager_db(BaseModel_db):
    #---Name
    __tablename__ = 'profit_manager'
    #---Items
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, default='')
    description = Column(String, default='')
    enable = Column(Boolean, default=True)
    #---Display
    def __repr__(self) : return f"{self.toDict()}"
    #---Json
    def toDict(self) : return {column.key: getattr(self, column.key) for column in inspect(self).mapper.column_attrs}

#--------------------------------------------------------------------------------- Python
class model_profit_manager_py(BaseModel_py):
    id : int = 0
    name : str = ''
    description : Optional[str] = ''
    enable : bool = True