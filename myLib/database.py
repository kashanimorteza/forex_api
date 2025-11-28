#--------------------------------------------------------------------------------- Location
# code/myLib/database.py

#--------------------------------------------------------------------------------- Description
# Database

#--------------------------------------------------------------------------------- Import
import re
import psycopg2
from myLib.utils import config, debug

#--------------------------------------------------------------------------------- Variable
dbData = {}
dbCfg = config.get("database", {}).get("main", {})
dbData["host"] = dbCfg.get("host", "127.0.0.1")
dbData["port"] = dbCfg.get("port", "5432")
dbData["user"] = dbCfg.get("user", "forex")
dbData["pass"] = dbCfg.get("pass", "123456")
dbData["name"] = dbCfg.get("name", "forex")

#--------------------------------------------------------------------------------- Action
class Database:
    #-------------------------- Constructor
    def __init__(self, dbHost=None, dbUser=None, dbPass=None, dbName=None, log=None): 
        self.className = "Database"
        methodName = "Init"

        if dbHost:
            self.dbHost=dbHost
            self.dbUser=dbUser
            self.dbPass=dbPass
            self.dbName=dbName
            self.dbConn = None
            self.dbCursor = None
            self.status = False
        else:
            self.dbHost=dbData["host"]
            self.dbUser=dbData["user"]
            self.dbPass=dbData["pass"]
            self.dbName=dbData["name"]
            self.dbConn = None
            self.dbCursor = None
            self.status = False

    #-------------------------- instance
    @classmethod
    def instance(cls):
        return cls()
    
    #-------------------------- open
    def open(self, connFree=None, name=None):
        """ open connection database """

        #----------------------------- Variable                
        methodName = "Open"
        #----------------------------- Execute        
        try:
            if self.status is False :
                if connFree: 
                    self.dbConn = psycopg2.connect(host=self.dbHost, user=self.dbUser, password=self.dbPass)
                else:
                    self.dbConn = psycopg2.connect(host=self.dbHost, user=self.dbUser, password=self.dbPass, database=self.dbName)
                self.dbConn.set_isolation_level(0)
                self.dbConn.autocommit = True                
                self.dbCursor = self.dbConn.cursor()
                self.status = True
                # if self.log is not None : 
                #     self.log.log('not',f'{self.className}({methodName}) ', name)            
        except Exception as e:
            self.status = False
            # if self.log is not None :
            #     self.log.log('err',f'{self.className}({methodName}) ', f"Host({self.dbHost}) | User({self.dbUser}) | Database({self.dbName}) | Error({re.sub(r'W+', ' ', str(e))})")
    
    #-------------------------- close
    def close(self, name=None):
        """ close connection database """

        #----------------------------- Variable                
        methodName = "Close"
        #----------------------------- Execute        
        try:
            if self.status :
                self.dbCursor.close()
                self.dbConn.close()
                self.status = False
                if self.log is not None : self.log.log('not',f'{self.className}({methodName})', name)
        except Exception as e:
            self.status = True
            # if self.log is not None :
            #     self.log.log('err',f'{self.className}({methodName})', f"Host({self.dbHost}) | User({self.dbUser}) | Database({self.dbName}) | Error({re.sub(r'W+', ' ', str(e))})")

    #-------------------------- execute
    def execute(self, cmd) :
        """ execute command """

        #----------------------------- Variable                
        methodName = "Execute"
        localDatabase =  False
        #----------------------------- Execute        
        try:
            #---Open
            if self.status is False:
                self.open()
                localDatabase =  True
            #---Execute
            self.dbCursor.execute(cmd)
            res = True
            #---Close            
            if self.status:
                if localDatabase:
                    self.close()                        
        except Exception as e:
            res = False
            error = str(e).replace('\n', ' ')
            # if self.log is not None :
            #     self.log.log('err', f'{self.className}({methodName})', f"cmd({cmd[:100]}) | Error({re.sub(r'W+', ' ', str(error))})") 
        return res

   #-------------------------- getData
    def getData(self, cmd):
        """ get list data """

        #----------------------------- Variable                
        methodName = "getData"
        localDatabase =  False   
        #----------------------------- Execute        
        try :
            #---Open
            if self.status is False:
                self.open()
                localDatabase =  True
            #---Execute
            self.dbCursor.execute(cmd)                           
            res = self.dbCursor.fetchall()
            #---Close            
            if self.status:
                if localDatabase:
                    self.close() 
        except Exception as e :
            res = False               
            # if self.log is not None :
            #     self.log.log('err',f'{self.className}({methodName})', f"Cmd({cmd[:100]}) | Error({re.sub(r'W+', ' ', str(e))})")
            
        return res

    #-------------------------- getDataOne
    def getDataOne(self, cmd):
        """ get single data """

        #----------------------------- Variable
        methodName = "getDataOne"
        localDatabase =  False
        #----------------------------- Execute
        try:
            #---Open
            if self.status is False:
                self.open()
                localDatabase =  True
            #---Execute
            self.dbCursor.execute(cmd)                                
            res = self.dbCursor.fetchone()
            if res is not None :
                res = res[0]
            #---Close            
            if self.status:
                if localDatabase:
                    self.close()                 
        except Exception as e:
            res = False
            # if self.log is not None :
            #     self.log.log('err',f'{self.className}({methodName})', f"Cmd({cmd[:100]}) | Error({re.sub(r'W+', ' ', str(e))})")

        return res