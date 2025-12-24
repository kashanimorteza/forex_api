#--------------------------------------------------------------------------------- Location
# webapi/routes/back_execute.py

#--------------------------------------------------------------------------------- Description
# This is route for back_execute

#--------------------------------------------------------------------------------- Import
import time
from logic.logic_util import sort
from logic.logic_util import model_output
from logic.logic_global import database_management
from fastapi import APIRouter, Request
from model.model_back_execute import model_back_execute_py as model_py
from model.model_back_execute import model_back_execute_db as model_db
from model.model_back_order import model_back_order_db as model_back_order_db
from logic.data_orm import Data_Orm
from logic.logic_backtest import Logic_BackTest

#--------------------------------------------------------------------------------- Action
#-------------------------- [Variable]
route = APIRouter()
data_orm = Data_Orm(database=database_management)
logic_backtest = Logic_BackTest()

#-------------------------- [Add]
@route.post("/add", description="add", response_model=model_output)
def add(item:model_py) : 
    item = item.dict()
    if 'id' in item : del item['id']
    output:model_output = data_orm.add(model=model_db, item=model_db(**item))
    return output

#-------------------------- [Items]
@route.get("/items", description="items", response_model=model_output)
def items(request: Request) : 
    filters = dict(request.query_params)
    output:model_output = data_orm.items(model=model_db, **filters)
    if output.status : 
        data = []
        for item in output.data : data.append(item.toDict())
        output.data = data
    return output

#-------------------------- [Update]
@route.put("", description="update", response_model=model_output)
def update(item: model_py): 
    return data_orm.update(model=model_db, item=model_db(**item.dict()))

#-------------------------- [Delete]
@route.delete("/{id}", description="delete", response_model=model_output)
def delete(id:int): 
    return data_orm.delete(model=model_db, id=id)

#-------------------------- [Enable]
@route.get("/enable/{id}", description="enable", response_model=model_output)
def enable(id:int): 
    return data_orm.enable(model=model_db, id=id)

#-------------------------- [Disable]
@route.get("/disable/{id}", description="disable", response_model=model_output)
def disable(id:int): 
    return data_orm.disable(model=model_db, id=id)

#-------------------------- [Status]
@route.get("/status/{id}", description="status", response_model=model_output)
def status(id:int): 
    return data_orm.status(model=model_db, id=id)

#-------------------------- [start]
@route.get("/start/{id}", description="start", response_model=model_output)
def start(id:int):
    start_time = time.time()
    logic_backtest.execute_id = id
    output:model_output = logic_backtest.run()
    output.time = sort(f"{(time.time() - start_time):.3f}", 3)
    return output