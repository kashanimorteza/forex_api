#--------------------------------------------------------------------------------- location
# webapi/routes/live_execute.py

#--------------------------------------------------------------------------------- Description
# This is route for live_execute

#--------------------------------------------------------------------------------- Import
import time
from myLib.utils import sort
from myLib.model import model_output
from myLib.logic_global import database_management
from fastapi import APIRouter, Request
from myModel.model_live_execute import model_live_execute_py as model_py
from myModel.model_live_execute import model_live_execute_db as model_db
from myLib.data_orm import Data_Orm
from myLib.logic_management import Logic_Management

#--------------------------------------------------------------------------------- Action
#-------------------------- [Variable]
route = APIRouter()
data_orm = Data_Orm(database=database_management)
logic_management = Logic_Management()

#-------------------------- [Add]
@route.post("/add", description="add", response_model=model_output)
def add(item:model_py) : 
    item = item.dict()
    if 'id' in item : del item['id']
    if 'date' in item : del item['date']
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

#-------------------------- [Dead]
@route.get("/dead/{id}", description="dead", response_model=model_output)
def dead(id:int): 
    return data_orm.dead(model=model_db, id=id)

#-------------------------- [start]
@route.get("/start/{id}", description="start", response_model=model_output)
def start(id:int):
    start_time = time.time()
    detaile = logic_management.execute_detaile(id=id)
    strategy_name = detaile.data.get("strategy_name")
    params = detaile.data.get("params")
    account_id = detaile.data.get("account_id")
    strategy = logic_management.get_strategy_item_instance(strategy_name=strategy_name, params=params, account_id=account_id).data
    output:model_output = strategy.start(id=id)
    output.time = sort(f"{(time.time() - start_time):.3f}", 3)
    return output

#-------------------------- [end]
@route.get("/stop/{id}", description="stop", response_model=model_output)
def end(id:int):
    start_time = time.time()
    detaile = logic_management.execute_detaile(id=id)
    strategy_name = detaile.data.get("strategy_name")
    params = detaile.data.get("params")
    account_id = detaile.data.get("account_id")
    strategy = logic_management.get_strategy_item_instance(strategy_name=strategy_name, params=params, account_id=account_id).data
    output:model_output = strategy.stop(id=id)
    output.time = sort(f"{(time.time() - start_time):.3f}", 3)
    return output