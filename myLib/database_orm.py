#--------------------------------------------------------------------------------- Location
# myLib/database_orm.py

#--------------------------------------------------------------------------------- Description
# database_orm

#--------------------------------------------------------------------------------- Import
from pyexpat import model
import inspect, time
from tty import CFLAG
from myLib.log import Log
from myLib.utils import config, debug
from myLib.model import model_output
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_, and_
from myLib.utils import debug, sort

#--------------------------------------------------------------------------------- Variable
BaseModel = declarative_base()
cfg = config.get("database", {}).get("main", {})
host = cfg.get("host")
port = cfg.get("port")
username = cfg.get("user")
password= cfg.get("pass",)
name = cfg.get("name")

#--------------------------------------------------------------------------------- Instance
engine = create_engine(f"postgresql://{username}:{password}@{host}:{port}/{name}", echo=False, pool_size=100, max_overflow=100)
session = sessionmaker(bind=engine)()

#--------------------------------------------------------------------------------- Class
class Database_Orm:
    #-------------------------- [Init]
    def __init__(
            self, 
            verbose: bool = False, 
            log: bool = False,  
            instance_log : Log =None
        ):
        #--------------------Variable
        self.this_class = self.__class__.__name__
        self.log = log
        self.verbose = verbose
        #--------------------Instance
        self.instance_log = instance_log if instance_log else Log()

    #-------------------------- [Create tables]
    def create_tables(self) -> model_output:
        import myModel
        BaseModel.metadata.create_all(engine)

    #-------------------------- [Add]
    def add(self, model, item, **filters) -> model_output:
        #--------------Description
        # IN     : model
        # OUT    : model_output
        # Action : add model to database
        try:
            #--------------Debug
            this_method = inspect.currentframe().f_code.co_name
            output = model_output()
            #--------------Variable
            #session = sessionmaker(bind=engine)()
            #--------------Data
            query = session.query(model)
            if filters:
                for attr, value in filters.items() : query = query.filter(getattr(model, attr) == value)
                item_exist = query.first()
            else:
                item_exist = query.filter(model.id == item.id).first()
            #--------------Action
            if not item_exist:
                session.add(item)
                session.commit()
                output.status = True
                output.data = {model.__name__: 'added'}
            else:
                output.status = False
                output.data = {model.__name__: 'exist'}
        except Exception as e:  
            #--------------Error
            output.status = False
            output.data = {"class":self.this_class, "method":this_method, "error": str(e)}
            print(output)
        # finally:
        #         session.close()
        #--------------Verbose
        if self.verbose : print(output)
        #--------------Log
        if self.log : print(output)
        #--------------Output
        return output
        
    #-------------------------- [Items]
    def items(self, model, **filters) -> model_output:
        #-------------- Description
        # IN     : 
        # OUT    : 
        # Action :
        #-------------- Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        start_time = time.time()
        #-------------- Output
        output = model_output()
        output.class_name = self.this_class
        output.method_name = this_method

        try:
            #--------------Action
            query = session.query(model)
            if filters:
                for attr, value in filters.items() : 
                    query = query.filter(getattr(model, attr) == value)
            query = query.order_by(model.id)
            result = query.all()
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.status = True if result else False
            output.message =f"{model}"
            output.data = result
            #--------------Verbose
            if verbose : self.instance_log.verbose("rep", f"{sort(self.this_class, 8)} | {sort(this_method, 8)} | {output.time}", output.message)
            #--------------Log
            if log : self.instance_log.log(log_model, output)
        except Exception as e:  
            #--------------Error
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.instance_log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.instance_log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Return
        return output

    #-------------------------- [Update]
    def update(self, model, item) -> model_output:
        #--------------Description
        # IN     : model
        # OUT    : model_output
        # Action : update model on database
        try:
            #--------------Debug
            this_method = inspect.currentframe().f_code.co_name
            output = model_output()
            #--------------Variable
            #session = sessionmaker(bind=self.engine)()
            #--------------Action
            source = session.query(model).filter(model.id == item.id).first()
            if source:
                for key, value in item.toDict().items():
                    if hasattr(source, key) : setattr(source, key, value)
                session.commit()
                output.status = True
                output.data = {model.__name__: f'updated:{item.id}'}
            else:
                output.status = False
                output.data = {model.__name__: f'updated:{item.id}'}
        except Exception as e:  
            #--------------Error
            output.status = False
            output.data = {"class":self.this_class, "method":this_method, "error": str(e)}
            print(output)
        # finally:
        #         session.close()
        #--------------Verbose
        if self.verbose : print(output)
        #--------------Log
        if self.log : print(output)
        #--------------Output
        return output

    #-------------------------- [Delete]
    def delete(self, model, id) -> model_output:
        #--------------Description
        # IN     : id
        # OUT    : model_output
        # Action : delete model from database
        try:
            #--------------Debug
            this_method = inspect.currentframe().f_code.co_name
            output = model_output()
            #--------------Variable
            #session = sessionmaker(bind=self.engine)()
            #--------------Data
            item = session.query(model).filter(model.id == id).first()
            #--------------Action
            if item:
                session.delete(item)
                session.commit()
                output.status = True
                output.data = {model.__name__: f'deleted:{id}'}
            else:
                output.status = False
                output.data = {model.__name__: f'not-exist:{id}'}
        except Exception as e:  
            #--------------Error
            output.status = False
            output.data = {"class":self.this_class, "method":this_method, "error": str(e)}
            print(output)
        # finally:
        #         session.close()
        #--------------Verbose
        if self.verbose : print(output)
        #--------------Log
        if self.log : print(output)
        #--------------Output
        return output

    #-------------------------- [Execute]
    def execute(self, model, cmd, values) -> model_output:
        #--------------Description
        # IN     : model
        # OUT    : model_output
        # Action : update model on database
        try:
            #--------------Debug
            this_method = inspect.currentframe().f_code.co_name
            output = model_output()
            #--------------Variable
            #session = sessionmaker(bind=self.engine)()
            #--------------Action
            sql = text(cmd)
            session.execute(sql, values)
            session.commit()
            output.data = {model.__name__: 'execute'}
        except Exception as e:  
            #--------------Error
            output.status = False
            output.data = {"class":self.this_class, "method":this_method, "error": str(e)}
            print(output)
        # finally:
        #         session.close()
        #--------------Verbose
        if self.verbose : print(output)
        #--------------Log
        if self.log : print(output)
        #--------------Output
        return output
    
    #-------------------------- [clear]
    def clear(self, model, **filters) -> model_output:
        #--------------Description
        # IN     : 
        # OUT    : model_output
        # Action : return list of models
        try:
            #--------------Debug
            this_method = inspect.currentframe().f_code.co_name
            output = model_output()
            #--------------Variable
            #session = sessionmaker(bind=self.engine)()
            #--------------Data
            query = session.query(model)
            if filters:
                for attr, value in filters.items() : 
                    query = query.filter(getattr(model, attr) == value)
            result = query.delete()
            session.commit()
            #--------------Output
            output.status = True if result else False
            output.data = result
        except Exception as e:  
            #--------------Error
            output.status = False
            output.data = {"class":self.this_class, "method":this_method, "error": str(e)}
            print(output)
        # finally:
        #         session.close()
        #--------------Verbose
        if self.verbose : print(output)
        #--------------Log
        if self.log : print(output)
        #--------------Output
        return output

    #-------------------------- [truncate]
    def truncate(self, model) -> model_output:
        #-------------- Description
        # IN     : 
        # OUT    : 
        # Action :
        #-------------- Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        start_time = time.time()
        #-------------- Output
        output = model_output()
        output.class_name = self.this_class
        output.method_name = this_method

        try:
            #--------------Action
            model.__table__.truncate(engine, checkfirst=True)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.message =f"Truncate table : {model}"
            #--------------Verbose
            if verbose : self.instance_log.verbose("rep", f"{sort(self.this_class, 8)} | {sort(this_method, 8)} | {output.time}", output.message)
            #--------------Log
            if log : self.instance_log.log(log_model, output)
        except Exception as e:  
            #--------------Error
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.instance_log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.instance_log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Return
        return output
    
    #-------------------------- [create]
    def create(self, model) -> model_output:
        #-------------- Description
        # IN     : 
        # OUT    : 
        # Action :
        #-------------- Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        start_time = time.time()
        #-------------- Output
        output = model_output()
        output.class_name = self.this_class
        output.method_name = this_method

        try:
            #--------------Action
            model.__table__.create(engine, checkfirst=True)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.message =f"Create table : {model}"
            #--------------Verbose
            if verbose : self.instance_log.verbose("rep", f"{sort(self.this_class, 8)} | {sort(this_method, 8)} | {output.time}", output.message)
            #--------------Log
            if log : self.instance_log.log(log_model, output)
        except Exception as e:  
            #--------------Error
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.instance_log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.instance_log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Return
        return output
    
    #-------------------------- [drop]
    def drop(self, model) -> model_output:
        #-------------- Description
        # IN     : 
        # OUT    : 
        # Action :
        #-------------- Debug
        this_method = inspect.currentframe().f_code.co_name
        verbose = debug.get(self.this_class, {}).get(this_method, {}).get('verbose', False)
        log = debug.get(self.this_class, {}).get(this_method, {}).get('log', False)
        log_model = debug.get(self.this_class, {}).get(this_method, {}).get('model', False)
        start_time = time.time()
        #-------------- Output
        output = model_output()
        output.class_name = self.this_class
        output.method_name = this_method

        try:
            #--------------Action
            model.__table__.drop(engine, checkfirst=True)
            #--------------Output
            output.time = sort(f"{(time.time() - start_time):.3f}", 3)
            output.message =f"Drop table : {model}"
            #--------------Verbose
            if verbose : self.instance_log.verbose("rep", f"{sort(self.this_class, 8)} | {sort(this_method, 8)} | {output.time}", output.message)
            #--------------Log
            if log : self.instance_log.log(log_model, output)
        except Exception as e:  
            #--------------Error
            output.status = False
            output.message = {"class":self.this_class, "method":this_method, "error": str(e)}
            self.instance_log.verbose("err", f"{self.this_class} | {this_method}", str(e))
            self.instance_log.log("err", f"{self.this_class} | {this_method}", str(e))
        #--------------Return
        return output
    
    #-------------------------- [pydantic_to_sqlalchemy]
    def pydantic_to_sqlalchemy(self, pydantic_instance, sqlalchemy_model):
        return sqlalchemy_model(**pydantic_instance.dict())

    #-------------------------- [sqlalchemy_to_pydantic]
    def sqlalchemy_to_pydantic(self, sqlalchemy_instance, pydantic_model):
        return pydantic_model(**sqlalchemy_instance.dict())