#--------------------------------------------------------------------------------- location
# webapi/routes/route_account.py

#--------------------------------------------------------------------------------- Description
# This is route for account

#--------------------------------------------------------------------------------- Import
from myLib.model import model_output
from fastapi import APIRouter, Request
from webapi.services.service import Service
from myModel.model_account import model_account_py as model_py
from myModel.model_account import model_account_db as model_db

#--------------------------------------------------------------------------------- Action
#-------------------------- [Variable]
route = APIRouter()
service = Service(model=model_db)

#-------------------------- [Add]
@route.post("/add", description="add", response_model=model_output)
def add(item:model_py) : 
    return service.add(item=item)

#-------------------------- [Items]
@route.get("/items", description="items", response_model=model_output)
def items(request: Request) : 
    filters = dict(request.query_params)
    return service.items(**filters)

#-------------------------- [Update]
@route.put("/update", description="update", response_model=model_output)
def update(item: model_py): 
    return service.update(item=item)

#-------------------------- [Delete]
@route.delete("/delete/{id}", description="delete", response_model=model_output)
def delete(id:int): 
    return service.delete(id=id)

#-------------------------- [Enable]
@route.get("/enable/{id}", description="enable", response_model=model_output)
def enable(id:int): 
    return service.enable(id=id)

#-------------------------- [Disable]
@route.get("/disable/{id}", description="disable", response_model=model_output)
def disable(id:int): 
    return service.disable(id=id)

#-------------------------- [Dead]
@route.get("/dead/{id}", description="dead", response_model=model_output)
def dead(id:int): 
    return service.dead(id=id)