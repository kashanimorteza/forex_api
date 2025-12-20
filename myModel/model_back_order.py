#--------------------------------------------------------------------------------- Location
# models/model_back_order.py

#--------------------------------------------------------------------------------- Description
# model_back_order

#--------------------------------------------------------------------------------- Import
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Sequence
from sqlalchemy.inspection import inspect
from sqlalchemy.sql import func
from myLib.database_orm import BaseModel as BaseModel_db
from pydantic import BaseModel as BaseModel_py
from typing import Optional
from datetime import datetime

#--------------------------------------------------------------------------------- Database
class model_back_order_db(BaseModel_db):
    #---Name
    __tablename__ = 'back_order'
    #---Items
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_open = Column(DateTime, default=func.now(), server_default=func.now())
    date_close = Column(DateTime, default=func.now(), server_default=func.now())
    execute_id = Column(Integer, default=0)
    order_id = Column(Integer, Sequence("back_order_order_id_seq"), nullable=False)
    trade_id = Column(Integer, Sequence("back_order_trade_id_seq"), nullable=False)
    symbol = Column(String, default='')
    action = Column(String, default='')
    amount = Column(Integer, default=0)
    bid = Column(Float, default=0.0)
    ask = Column(Float, default=0.0)
    price_open = Column(Float, default=0.0)
    price_close = Column(Float, default=0.0)
    tp = Column(Float, default=0.0)
    sl = Column(Float, default=0.0)
    profit = Column(Float, default=0.0)
    status = Column(String, default='')
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
class model_back_order_py(BaseModel_py):
    id : int = 0
    date_open : Optional[str] = ''
    date_close : Optional[str] = ''
    execute_id : int = 0
    order_id : int = 0
    trade_id : int = 0
    symbol : str = ''
    action : str = ''
    amount : int = 0
    bid : float = 0
    ask : float = 0
    price_open : float = 0
    price_close : float = 0
    tp : float = 0
    sl : float = 0
    profit : float = 0
    status : str = ''
    description : Optional[str] = ''
    enable : bool = True