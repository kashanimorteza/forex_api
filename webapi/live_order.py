#--------------------------------------------------------------------------------- location
# webapi/live_order.py

#--------------------------------------------------------------------------------- Description
# This is route for live_order

#--------------------------------------------------------------------------------- Import
import time
from logic.logic_util import model_output
from logic.logic_global import database_management
from fastapi import APIRouter, Request
from model.model_live_order import model_live_order_py as model_py
from model.model_live_order import model_live_order_db as model_db
from logic.data_orm import Data_Orm
from logic.logic_live import Logic_Live

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
    if 'date' in item : del item['date']
    output:model_output = data_orm.add(model=model_db, item=model_db(**item))
    return output

#-------------------------- [Items]
@route.get("/items", description="items", response_model=model_output)
def items(request: Request) : 
    filters = dict(request.query_params)
    output:model_output = data_orm.items(model=model_db, order_by={"status":"desc","date":"desc"}, **filters)
    if output.status : 
        data = []
        for item in output.data : 
            i = item.toDict()
            #i["amount"] = i["amount"]/ 100000 
            data.append(i)
        output.data = data
    return output

#-------------------------- [Update]
@route.put("", description="update", response_model=model_output)
def update(item: model_py): 
    return data_orm.update(model=model_db, item=model_db(**item.dict()))

#-------------------------- [Delete]
@route.delete("/{id}", description="delete", response_model=model_output)
def delete(id): 
    return data_orm.delete(model=model_db, id=id)

#-------------------------- [Enable]
@route.get("/enable/{id}", description="enable", response_model=model_output)
def enable(id): 
    return data_orm.enable(model=model_db, id=id)

#-------------------------- [Disable]
@route.get("/disable/{id}", description="disable", response_model=model_output)
def disable(id): 
    return data_orm.disable(model=model_db, id=id)

#-------------------------- [Status]
@route.get("/status/{id}", description="status", response_model=model_output)
def status(id): 
    return data_orm.status(model=model_db, id=id)

#-------------------------- [order_clear]
@route.get("/order_clear/{id}", description="order_clear", response_model=model_output)
def order_clear(id): 
    return logic_live.order_clear(execute_id=id)

#-------------------------- [count]
@route.get("/order_count/{id}", description="order_count", response_model=int)
def order_count(id): 
    result = logic_live.order_count(execute_id=id)
    return result

#-------------------------- [Detaile]
@route.get("/detaile", description="detaile", response_model=model_output)
def detaile(request: Request) : 
    start_time = time.time()
    filters = dict(request.query_params)
    id = int(filters.get('execute_id'))
    output = logic_live.execute_order_detaile(id=id)
    output.time = f"{(time.time() - start_time):.3f}",
    return output


