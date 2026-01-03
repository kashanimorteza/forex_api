#--------------------------------------------------------------------------------- Location
# logic/logic_log.py

#--------------------------------------------------------------------------------- Description
# Logic_Log

#--------------------------------------------------------------------------------- Import
import inspect, re
from datetime import datetime as dt
from logic.util import sort

#--------------------------------------------------------------------------------- Action
class Logic_Log:
    #------------------------------------------------------------------- [ Constructor ]
    def __init__(self, config, db=None):
        #-------------- Variable
        self.this_class = self.__class__.__name__
        self.className = self.this_class
        self.config = config
        self.db = db
        #--------------------------------- General
        generalCfg = config.get("log", {}).get("general", {})
        self.fileName = generalCfg.get("file", "n")
        self.tblName = generalCfg.get("table", "n")
        #--------------------------------- Error
        errorCfg = config.get("log", {}).get("error", {})
        self.err_verbose = errorCfg.get("verbose", "False")
        self.err_toFile = errorCfg.get("file", "False")
        self.err_toDatabase = errorCfg.get("database", "False")
        #--------------------------------- Notification
        notificationCfg = config.get("log", {}).get("notification", {})
        self.not_verbose = notificationCfg.get("verbose", "False")
        self.not_toFile = notificationCfg.get("file", "False")
        self.not_toDatabase = notificationCfg.get("database", "False")
        #--------------------------------- Report
        reportCfg = config.get("log", {}).get("report", {})
        self.rep_verbose = reportCfg.get("verbose", "False")
        self.rep_toFile = reportCfg.get("file", "False")
        self.rep_toDatabase = reportCfg.get("database", "False")
        #--------------------------------- Object
        self.fileOpen()

    #------------------------------------------------------------------- [ Database ]
    def database(self, drop, create, add):
        
        #--------------------------------- variable
        methodName = inspect.currentframe().f_code.co_name
        res = False
        db =self.db
        #--------------------------------- execution
        try:
            res=db.getDataOne(f"SELECT oid FROM pg_database WHERE datname='{self.dbName}'")
            if drop and res!=None:
                res = db.execute(f'DROP DATABASE "{self.dbName}"')                
                self.verbose('not',f'{self.className}({methodName}) ', f'Drop Database {self.dbName} : {res}')
                res=None
            if create and res==None:                
                res = db.execute(f'CREATE DATABASE "{self.dbName}"')                
                self.verbose('not',f'{self.className}({methodName}) ', f'Create Database {self.dbName} : {res}')                       
            res = True
        except Exception as e:
            res = False
            self.verbose('err', f'{self.className}({methodName}) ', f"Database({self.dbName}) | Drop({drop}) | Create({create}) | Add({add}) | Error({re.sub(r'W+', ' ', str(e))})")            
        return res
        
    #------------------------------------------------------------------- [ Table ]    
    def table(self, drop, create, add):
        
        #--------------------------------- variable        
        methodName = "Table"
        res = False       
        #--------------------------------- execution
        try:                                                           
            if drop:                
                res = self.db.db.execute(f"DROP TABLE IF EXISTS {self.tblName}")                
                self.verbose('not',f'{self.className}({methodName})    ', f'Drop Table {self.tblName} : {res}')
            if create:
                query = f"""CREATE TABLE IF NOT EXISTS {self.tblName}
                (
                id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
                date text,
                model text NOT NULL,
                subject text NOT NULL,            
                data text,           
                PRIMARY KEY (id)
                );"""                
                res = self.db.db.execute(query)                
                self.verbose('not',f'{self.className}({methodName})    ',f'Create Table {self.tblName} : {res}')                                
            res = True
        except Exception as e:
            res = False
            self.verbose('err', f'{self.className}({methodName})    ', f"Table:{self.tblName} | Drop:{drop} | Create({create}) | Add({add}) | Error({re.sub(r'W+', ' ', str(e))})")            

        return res

    #------------------------------------------------------------------- [ Log ]    
    def log(self, model, subject, data):

        #--------------------------------- variable        
        methodName = "Log"
        res = False        
        #--------------------------------- execution        
        try:                        
            #----------- verbose
            self.verbose(model, subject, data)
            #----------- toFile        
            self.toFile(model, subject, data)                       
            #----------- toDatabase             
            #self.toDatabase(model, subject, data)
            res = True
        except Exception as e:
            res = False
            self.verbose('err', f'{self.className}({methodName})', f"Model:{model} | Subject({subject}) | Data({data}) | Error({re.sub(r'W+', ' ', str(e))})")            
            
        return res

    #------------------------------------------------------------------- [ Verbose ]    
    def verbose (self, model, subject, data):

        #--------------------------------- variable        
        methodName = "Verbose"
        res = False
        #--------------------------------- execution        
        try:
            msg = f"{dt.now():%Y-%m-%d %H:%M:%S} | {sort(model, 3)} | {sort(subject, 30)} | {data}"
            if model=='err' and self.err_verbose: print(msg, flush=True)
            if model=='not' and self.not_verbose: print(msg, flush=True)
            if model=='rep' and self.rep_verbose: print(msg, flush=True)
            res = True
        except Exception as e:
            res = False
            self.verbose('err', f'{self.className}({methodName})', f"Model:{model} | Subject({subject}) | Data({data}) | Error({re.sub(r'W+', ' ', str(e))})")

        return res
    
    #------------------------------------------------------------------- [ toDatabase ]    
    def toDatabase (self, model, subject, data):

        #--------------------------------- variable        
        methodName = "toDatabase"
        res = False
        if self.db.db.status !=True:
            self.db.db.open()
        #--------------------------------- execution        
        try:
            if data is not None:      
                data = data.replace("\"","")
                data = data.replace("'","")
                data = data.replace("^","")  
            if model=='err' and self.err_toDatabase:                     
                    self.db.db.execute(f"INSERT INTO {self.tblName} (date, model, subject, data) VALUES('{dt.now():%Y-%m-%d %H:%M:%S}', '{model}', '{subject}', '{data}')")
            if model=='not' and self.not_toDatabase:                     
                    self.db.db.execute(f"INSERT INTO {self.tblName} (date, model, subject, data) VALUES('{dt.now():%Y-%m-%d %H:%M:%S}', '{model}', '{subject}', '{data}')")
            if model=='rep' and self.not_toDatabase:                     
                    self.db.db.execute(f"INSERT INTO {self.tblName} (date, model, subject, data) VALUES('{dt.now():%Y-%m-%d %H:%M:%S}', '{model}', '{subject}', '{data}')")
            res = True
        except Exception as e:
            res = False
            self.verbose('err', f'{self.className}({methodName})', f"Model:{model} | Subject({subject}) | Data({data}) | Error({re.sub(r'W+', ' ', str(e))})")

        return res

    #------------------------------------------------------------------- [ File ]
    #--------------------------------- toFile
    def toFile (self, model, subject, data):

        #------------- variable         
        methodName = "toFile"
        res = False
        #------------- execution        
        try:
            #self.fileOpen()
            subject = '{:<16}'.format(subject)  
            msg = f"\n{dt.now():%Y-%m-%d %H:%M:%S} | {model} | {subject} | {data}"     
            if model=='err' and self.err_toFile :                              
                    self.fle.write(msg) 
                    self.fle.flush()
            if model=='not' and self.not_toFile:                             
                    self.fle.write(msg)
                    self.fle.flush()
            if model=='rep' and self.rep_toFile:                           
                    self.fle.write(msg)
                    self.fle.flush()
            #self.fileClose()
            res = True
        except Exception as e:
            res = False
            self.verbose('err', f'{self.className}({methodName})', f"Model:{model} | Subject({subject}) | Data({data}) | Error({re.sub(r'W+', ' ', str(e))})")

        return res

    #--------------------------------- fileClear
    def fileClear(self) :

        #------------- variable        
        methodName = "fileClear"
        res = False
        #------------- execution        
        try:            
            #self.fileOpen()
            self.fle.truncate(0)
            #self.fileClose()
            res = True
            self.verbose('not', f'{self.className}({methodName})', f"File Cleared : {self.fileName}")
        except Exception as e:
            res = False
            self.verbose('err', f'{self.className}({methodName})', f"Error({re.sub(r'W+', ' ', str(e))})")                        

        return res

    #--------------------------------- fileOpen
    def fileOpen(self) : 

        #------------- variable        
        methodName = "fileOpen"
        res = False
        #------------- execution
        try:                     
            self.fle = open(self.fileName, 'a')
            self.FileStatus = True
            res = True             
        except Exception as e:
            res = False
            self.verbose('err', f'{self.className}({methodName})', f"Error({re.sub(r'W+', ' ', str(e))})")            

        return res    

    #--------------------------------- fileClose
    def fileClose(self) :

        #------------- variable        
        methodName = "fileClose"
        res = False
        #------------- execution
        try:            
            self.fle.close()
            res = True
        except Exception as e:
            res = False
            self.verbose('err', f'{self.className}({methodName})', f"Error({re.sub(r'W+', ' ', str(e))})")            

        return res