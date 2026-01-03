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
class model_live_order_db(BaseModel_db):
    #---Name
    __tablename__ = 'live_order'
    #---Items
    id = Column(Integer, primary_key=True, autoincrement=True)
    execute_id = Column(Integer, default=1)
    step = Column(Integer, default=1)
    father_id = Column(Integer, default=0)
    date_open = Column(DateTime)
    price_open = Column(Float, default=0.0)
    date_close = Column(DateTime)
    price_close = Column(Float, default=0.0)
    profit = Column(Float, default=0.0)
    status = Column(String, default='')
    symbol = Column(String, default='')
    action = Column(String, default='')
    amount = Column(Integer, default=0)
    tp = Column(Float, default=0.0)
    sl = Column(Float, default=0.0)
    order_id = Column(String, default='')
    trade_id = Column(String, default='')
    description = Column(String, default='')
    enable = Column(Boolean, default=True)
    #---Display
    def __repr__(self) : return f"{self.toDict()}"
    #---Json
    def toDict(self):
        data = {column.key: getattr(self, column.key) for column in inspect(self).mapper.column_attrs}
        if data.get('date_open') and isinstance(data['date_open'], datetime) : data['date_open'] = data['date_open'].strftime('%Y-%m-%d %H:%M:%S')
        if data.get('date_close') and isinstance(data['date_close'], datetime) : data['date_close'] = data['date_close'].strftime('%Y-%m-%d %H:%M:%S')
        return data

#--------------------------------------------------------------------------------- Python
class model_live_order_py(BaseModel_py):
    id : int = 0
    execute_id : int = 1
    step : int = 1
    father_id : int = 0
    date_open : Optional[str] = ''
    price_open : float = 0
    date_close : Optional[str] = ''
    price_close : float = 0
    profit : float = 0
    status : str = ''
    symbol : str = ''
    action : str = ''
    amount : int = 0
    tp : float = 0
    sl : float = 0
    order_id : int = 0
    trade_id : int = 0
    description : Optional[str] = ''
    enable : bool = True