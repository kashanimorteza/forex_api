#--------------------------------------------------------------------------------- location
# webapi/live_execute.py

#--------------------------------------------------------------------------------- Description
# This is route for live_execute

#--------------------------------------------------------------------------------- Import
from logic.util import model_output
from logic.startup import database_management, Strategy_Action
from fastapi import APIRouter, Request
from model.live_execute import model_live_execute_py as model_py
from model.live_execute import model_live_execute_db as model_db
from model.live_order import model_live_order_db as model_order_db
from logic.data_orm import Data_Orm
from logic.live import Logic_Live

#--------------------------------------------------------------------------------- Action
#-------------------------- [Variable]
route = APIRouter()
data_orm = Data_Orm(database=database_management)
logic_live = Logic_Live()

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
@route.get("/start/{execute_id}", description="start", response_model=model_output)
def start(execute_id:int):
    output:model_output = logic_live.strategy_action(execute_id=execute_id, action=Strategy_Action.START)
    return output

#-------------------------- [end]
@route.get("/stop/{execute_id}", description="stop", response_model=model_output)
def stop(execute_id:int):
    output:model_output = logic_live.strategy_action(execute_id=execute_id, action=Strategy_Action.STOP)
    return output

#-------------------------- [order_clear]
@route.get("/order_clear/{id}", description="order_clear", response_model=model_output)
def order_clear(id:int): 
    return logic_live.order_clear(execute_id=id)

#-------------------------- [order_truncate]
@route.get("/order_truncate", description="order_truncate", response_model=model_output)
def order_truncate(): 
    return logic_live.order_truncate()

#-------------------------- [execute_step]
@route.get("/execute_step/{id}", description="execute_step", response_model=int)
def execute_step(id:int): 
    result = logic_live.execute_step(execute_id=id)
    return result

#-------------------------- [action_detaile]
@route.get("/action_detaile/{execute_id}", description="action_detaile", response_model=model_output)
def action_detaile(execute_id:int): 
    result = logic_live.action_detaile(execute_id=execute_id)
    return result

#-------------------------- [order_item]
@route.get("/order_item", description="order_item", response_model=model_output)
def order_item(request: Request) : 
    filters = dict(request.query_params)
    result = logic_live.order_item(**filters)
    return result