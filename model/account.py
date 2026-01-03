#--------------------------------------------------------------------------------- Location
# model/model_account.py

#--------------------------------------------------------------------------------- Description
# model_account

#--------------------------------------------------------------------------------- Import
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.inspection import inspect
from logic.database_orm import BaseModel as BaseModel_db
from pydantic import BaseModel as BaseModel_py
from typing import Optional

#--------------------------------------------------------------------------------- Database
class model_account_db(BaseModel_db):
    #---Name
    __tablename__ = 'account'
    #---Items
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, default='')
    broker = Column(String, default='FXCM')
    type = Column(String, default='Demo')
    currency = Column(String, default='USD')
    server = Column(String, default='FXCM-GBPReal01')
    username = Column(String, default='')
    password = Column(String, default='')
    url = Column(String, default='http://www.fxcorporate.com/Hosts.jsp')
    key = Column(String, default='')
    description = Column(String, default='')
    enable = Column(Boolean, default=True)
    #---Display
    def __repr__(self) : return f"{self.toDict()}"
    #---Json
    def toDict(self) : return {column.key: getattr(self, column.key) for column in inspect(self).mapper.column_attrs}

#--------------------------------------------------------------------------------- Python
class model_account_py(BaseModel_py):
    id : int = 0
    name : str = ''
    broker : str = 'FXCM'
    type : str = 'Demo'
    currency : str = 'USD'
    server : str = 'FXCM-GBPReal01'
    username : str = ''
    password : str = ''
    url : str = 'http://www.fxcorporate.com/Hosts.jsp'
    key : str = ''
    description : Optional[str] = ''
    enable : bool = True