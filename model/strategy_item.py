#--------------------------------------------------------------------------------- Location
# models/model_strategy_item.py

#--------------------------------------------------------------------------------- Description
# model_strategy_item

#--------------------------------------------------------------------------------- Import
from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.inspection import inspect
from logic.database_orm import BaseModel as BaseModel_db
from pydantic import BaseModel as BaseModel_py
from typing import Optional

#--------------------------------------------------------------------------------- Database
class model_strategy_item_db(BaseModel_db):
    #---Name
    __tablename__ = 'strategy_item'
    #---Items
    id = Column(Integer, primary_key=True, autoincrement=True)
    strategy_id = Column(Integer, default=0)
    name = Column(String, default='')
    symbols = Column(String, default='')
    actions = Column(String, default='')
    amount = Column(Integer, default=0)
    tp_pips = Column(Integer, default=0)
    sl_pips = Column(Integer, default=0)
    limit_trade = Column(Integer, default=0)
    limit_profit = Column(Integer, default=0)
    limit_loss = Column(Integer, default=0)
    params = Column(String, default='')
    description = Column(String, default='')
    enable = Column(Boolean, default=True)
    #---Display
    def __repr__(self) : return f"{self.toDict()}"
    #---Json
    def toDict(self) : return {column.key: getattr(self, column.key) for column in inspect(self).mapper.column_attrs}

#--------------------------------------------------------------------------------- Python
class model_strategy_item_py(BaseModel_py):
    id : int = 0
    strategy_id : int = 0
    name : str = ''
    symbols : str = ''
    actions : str = ''
    amount : int = 0
    tp_pips : int = 0
    sl_pips : int = 0
    limit_trade : int = 0
    limit_profit : int = 0
    limit_loss : int = 0
    params : str = ''
    description : Optional[str] = ''
    enable : bool = True