#--------------------------------------------------------------------------------- Location
# model/model_instrument.py

#--------------------------------------------------------------------------------- Description
# model_instrument

#--------------------------------------------------------------------------------- Import
from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.inspection import inspect
from logic.database_orm import BaseModel as BaseModel_db
from pydantic import BaseModel as BaseModel_py
from typing import Optional

#--------------------------------------------------------------------------------- Database
class model_instrument_db(BaseModel_db):
    #---Name
    __tablename__ = 'instrument'
    #---Items
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    instrument = Column(String, default='')
    category = Column(Integer, default=0)
    priority = Column(Integer, default=0)
    point_size = Column(Float, default=0.0)
    digits = Column(Integer, default=0)
    description = Column(String, default='')
    enable = Column(Boolean, default=True)
    #---Display
    def __repr__(self) : return f"{self.toDict()}"
    #---Json
    def toDict(self) : return {column.key: getattr(self, column.key) for column in inspect(self).mapper.column_attrs}

#--------------------------------------------------------------------------------- Python
class model_instrument_py(BaseModel_py):
    id : int = 0
    name : str = ''
    instrument : str = ''
    category : int = 0
    priority : int = 0
    point_size : float = 0.0
    digits : int = 0
    description : Optional[str] = ''
    enable : bool = True