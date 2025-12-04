#--------------------------------------------------------------------------------- Location
# models/strategy_item_trade.py

#--------------------------------------------------------------------------------- Description
# strategy_item_trade

#--------------------------------------------------------------------------------- Import
from sqlalchemy import Column, Integer, String, Boolean,Float
from sqlalchemy.inspection import inspect
from myLib.database_orm import BaseModel as BaseModel_db
from pydantic import BaseModel as BaseModel_py
from typing import Optional

#--------------------------------------------------------------------------------- Database
class strategy_item_trade_model_db(BaseModel_db):
    #---Name
    __tablename__ = 'strategy_item_trade'
    #---Items
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(String, default='')
    strategy_item_id = Column(Integer, default=0)
    symbol = Column(String, default='')
    action = Column(String, default='')
    amount = Column(Integer, default=0)
    price = Column(Float, default=0.0)
    tp = Column(Float, default=0.0)
    sl = Column(Float, default=0.0)
    open = Column(Boolean, default=True)
    description = Column(String, default='')
    enable = Column(Boolean, default=True)
    #---Display
    def __repr__(self) : return f"{self.toDict()}"
    #---Json
    def toDict(self) : return {column.key: getattr(self, column.key) for column in inspect(self).mapper.column_attrs}

#--------------------------------------------------------------------------------- Python
class strategy_item_trade_model_py(BaseModel_py):
    id : int = 0
    order_id : str = ''
    strategy_item_id : int = 0
    symbol : str = ''
    action : str = ''
    amount : int = 0
    price : float = 0
    tp : float = 0
    sl : float = 0
    open : bool = True
    description : Optional[str] = ''
    enable : bool = True