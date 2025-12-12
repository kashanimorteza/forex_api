#--------------------------------------------------------------------------------- location
# webapi/routes/live_order.py

#--------------------------------------------------------------------------------- Description
# This is route for live_order

#--------------------------------------------------------------------------------- Import
from myLib.model import model_output
from myLib.logic_live_execute import Logic_Test_Live
from fastapi import APIRouter, Request
from myModel.model_live_order import model_live_order_py as model_py
from myModel.model_live_order import model_live_order_db as model_db
from myLib.data_orm import Data_Orm

#--------------------------------------------------------------------------------- Action
#-------------------------- [Variable]
route = APIRouter()
data_orm = Data_Orm()
logic_test_live = Logic_Test_Live(instance_data_orm=data_orm)

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
    return logic_test_live.start(id=id)

#-------------------------- [end]
@route.get("/end/{id}", description="end", response_model=model_output)
def end(id:int):
    return logic_test_live.end(id=id)

#-------------------------- [order_close]
@route.get("/order_close/{id}", description="order_close", response_model=model_output)
def order_close(id:int):
    return logic_test_live.order_close(id=id)

#-------------------------- [price_change]
@route.get("/price_change/{id}", description="price_change", response_model=model_output)
def price_change(id:int):
    return logic_test_live.price_change(id=id)
