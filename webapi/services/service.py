#--------------------------------------------------------------------------------- location
# webapi/services/service.py

#--------------------------------------------------------------------------------- Description
# Service

#--------------------------------------------------------------------------------- Import
from myLib.model import model_output
from myLogic.logic import Logic

#--------------------------------------------------------------------------------- service
class Service:
    #-------------------------- [Init]
    def __init__(self, model) : 
        self.model = model
        self.logic = Logic(model=model)

    #-------------------------- [Add]
    def add(self, item) -> model_output:
        item = item.dict()
        del item['id']
        item = self.model(**item)
        output:model_output = self.logic.add(item=item)
        return output

    #-------------------------- [Items]
    def items(self) -> model_output:
        output:model_output = self.logic.items()
        if output.status : 
            data = []
            for item in output.data : data.append(item.toDict())
            output.data = data
        return output

    #-------------------------- [Item]
    def item(self,id:int) -> model_output:
        output:model_output = self.logic.item(id=id)
        if output.status : 
            output.data = output.data[0].toDict()
        return output
    
    #-------------------------- [Update]
    def update(self, item) -> model_output:
        return self.logic.update(item=self.model(**item.dict()))

    #-------------------------- [Delete]
    def delete(self, id:int) -> model_output:
        return self.logic.delete(id=id)

    #-------------------------- [Enable]
    def enable(self, id:int) -> model_output:
        return self.logic.enable(id=id)

    #-------------------------- [Disable]
    def disable(self, id:int) -> model_output:
        return self.logic.disable(id=id)

    #-------------------------- [Dead]
    def dead(self, id:int) -> model_output:
        return self.logic.dead(id=id)