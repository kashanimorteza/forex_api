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
        # Remove date if it's None or empty string to use database default
        if 'date' in item and (item['date'] is None or item['date'] == ''):
            del item['date']
        item = self.model(**item)
        output:model_output = self.logic.add(item=item)
        return output

    #-------------------------- [Items]
    def items(self, **filters) -> model_output:
        output:model_output = self.logic.items(**filters)
        if output.status : 
            data = []
            for item in output.data : data.append(item.toDict())
            output.data = data
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

    #-------------------------- [Status]
    def status(self, id:int) -> model_output:
        return self.logic.status(id=id)
    
    #-------------------------- [Dead]
    def dead(self, id:int) -> model_output:
        return self.logic.dead(id=id)