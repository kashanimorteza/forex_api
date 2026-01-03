#--------------------------------------------------------------------------------- Location
# models/model_profit_manager_item.py

#--------------------------------------------------------------------------------- Description
# model_profit_manager_item

#--------------------------------------------------------------------------------- Import
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.inspection import inspect
from logic.database_orm import BaseModel as BaseModel_db
from pydantic import BaseModel as BaseModel_py
from typing import Optional

#--------------------------------------------------------------------------------- Database
class model_profit_manager_item_db(BaseModel_db):
    #---Name
    __tablename__ = 'profit_manager_item'
    #---Items
    id = Column(Integer, primary_key=True, autoincrement=True)
    profit_manager_id = Column(Integer, default=1)
    name = Column(String, default='')
    value = Column(Integer, default=1)
    tp_value = Column(Integer, default=0)
    sl_value = Column(Integer, default=0)
    description = Column(String, default='')
    enable = Column(Boolean, default=True)
    #---Display
    def __repr__(self) : return f"{self.toDict()}"
    #---Json
    def toDict(self) : return {column.key: getattr(self, column.key) for column in inspect(self).mapper.column_attrs}

#--------------------------------------------------------------------------------- Python
class model_profit_manager_item_py(BaseModel_py):
    id : int = 0
    profit_manager_id : int = 1
    name : str = ''
    value : int = 1
    tp_value : int = 0
    sl_value : int = 0
    description : Optional[str] = ''
    enable : bool = True