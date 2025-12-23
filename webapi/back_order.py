#--------------------------------------------------------------------------------- location
# webapi/routes/back_order.py

#--------------------------------------------------------------------------------- Description
# This is route for back_order

#--------------------------------------------------------------------------------- Import
from myLib.utils import model_output
from myLib.logic_global import database_management
from fastapi import APIRouter, Request
from myModel.model_back_order import model_back_order_py as model_py
from myModel.model_back_order import model_back_order_db as model_db
from myLib.data_orm import Data_Orm
from myLib.logic_backtest import Logic_BackTest

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
    if 'date' in item : del item['date']
    output:model_output = data_orm.add(model=model_db, item=model_db(**item))
    return output

#-------------------------- [Items]
@route.get("/items", description="items", response_model=model_output)
def items(request: Request) : 
    filters = dict(request.query_params)
    output:model_output = data_orm.items(model=model_db, order_by={"id":"asc",}, **filters)
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
    return logic_backtest.order_clear(execute_id=id)

#-------------------------- [count]
@route.get("/order_count/{id}", description="order_count", response_model=int)
def order_count(id): 
    result = logic_backtest.order_count(execute_id=id)
    return result

#-------------------------- [Detaile]
@route.get("/detaile/{id}", description="detaile", response_model=model_output)
def detaile(id): 
    result = logic_backtest.order_detaile(execute_id=id)
    return result
