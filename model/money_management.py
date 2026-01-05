#--------------------------------------------------------------------------------- Location
# model/money_management.py

#--------------------------------------------------------------------------------- Description
# money_management

#--------------------------------------------------------------------------------- Import
from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.inspection import inspect
from logic.database_orm import BaseModel as BaseModel_db
from pydantic import BaseModel as BaseModel_py
from typing import Optional

#--------------------------------------------------------------------------------- Database
class model_money_management_db(BaseModel_db):
    #---Name
    __tablename__ = 'money_management'
    #---Items
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, default='')
    balance = Column(Integer, default=1000)
    risk = Column(Integer, default=1000)
    limit_trade = Column(Integer, default=-1)
    limit_profit = Column(Integer, default=-1)
    limit_loss = Column(Integer, default=-1)
    description = Column(String, default='')
    enable = Column(Boolean, default=True)
    #---Display
    def __repr__(self) : return f"{self.toDict()}"
    #---Json
    def toDict(self) : return {column.key: getattr(self, column.key) for column in inspect(self).mapper.column_attrs}

#--------------------------------------------------------------------------------- Python
class model_money_management_py(BaseModel_py):
    id : int = 0
    name : str = ''
    balance : int = 1000
    risk : int = 1
    limit_trade : int = -1
    limit_profit : int = -1
    limit_loss : int = -1
    description : Optional[str] = ''
    enable : bool = True