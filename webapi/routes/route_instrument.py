#--------------------------------------------------------------------------------- location
# webapi/routes/route_instrument.py

#--------------------------------------------------------------------------------- Description
# This is route for instrument

#--------------------------------------------------------------------------------- Import
from myLib.model import model_output
from fastapi import APIRouter
from webapi.services.service import Service
from myModel.model_instrument import model_instrument_py as model

#--------------------------------------------------------------------------------- Action
#-------------------------- [Variable]
route = APIRouter()
service = Service(model=model)

#-------------------------- [Add]
@route.post("/add", description="add", response_model=model_output)
def add(item:model) : 
    return service.add(item=item)

#-------------------------- [Items]
@route.get("/items", description="items", response_model=model_output)
def items() : 
    return service.items()

#-------------------------- [Item]
@route.get("/item/{id}", description="item", response_model=model_output)
def item(id:int) : 
    return service.item(id=id)

#-------------------------- [Update]
@route.put("/update", description="update", response_model=model_output)
def update(item: model): 
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