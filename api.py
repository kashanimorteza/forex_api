#--------------------------------------------------------------------------------- location
# webapi.py

#--------------------------------------------------------------------------------- Description
# This is main file of webapi

#--------------------------------------------------------------------------------- Import
#--------------------------------------------- Warnings
import logging, warnings
warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("root").setLevel(logging.CRITICAL)
#--------------------------------------------- Other
import uvicorn
import threading
from logic.logic_global import config, load_forex_api, list_close
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from webapi import *
from listen_close import Listen_Close
from listen_close_execute import Listen_Close_Execute
from logic.logic_live import Logic_Live

#--------------------------------------------------------------------------------- Variable
title = config.get("webapi", {}).get("title", {})
description = config.get("webapi", {}).get("description", {})
version = config.get("webapi", {}).get("version", {})
openapi_url = config.get("webapi", {}).get("openapi_url", {})
docs_url = config.get("webapi", {}).get("docs_url", {})
redoc_url = config.get("webapi", {}).get("redoc_url", {})
key = config.get("webapi", {}).get("key", {})
host = config.get("webapi", {}).get("host", {})
port = config.get("webapi", {}).get("port", {})
load_forex_api()

#--------------------------------------------------------------------------------- App
app = FastAPI(
    title = title,
    description = description,
    version=version,
    openapi_url=f"/{key}{openapi_url}",
    docs_url=f"/{key}{docs_url}",
    redoc_url=f"/{key}{redoc_url}"
)
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"]
)

#--------------------------------------------------------------------------------- Listeners
listener_close = None
listener_close_execute = None
listener_thread = None
listener_execute_thread = None
logic_live = Logic_Live(account_id=2)

@app.on_event("startup")
async def startup_event():
    global listener_close, listener_close_execute, listener_thread, listener_execute_thread
    from logic.logic_global import forex_apis
    
    # Start Listen_Close
    listener_close = Listen_Close(forex=logic_live, items=list_close)
    listener_thread = threading.Thread(target=listener_close.start, daemon=True)
    listener_thread.start()
    
    # Start Listen_Close_Execute
    listener_close_execute = Listen_Close_Execute(items=list_close, sleep_time=0.25)
    listener_execute_thread = threading.Thread(target=listener_close_execute.start, daemon=True)
    listener_execute_thread.start()

@app.on_event("shutdown")
async def shutdown_event():
    global listener_close
    if listener_close:
        listener_close.stop()
        
#--------------------------------------------------------------------------------- Route
routes = [
    (account, f"/{key}/account", ["Account"]),
    (instrument, f"/{key}/instrument", ["Instrument"]),
    (strategy, f"/{key}/strategy", ["Strategy"]),
    (strategy_item, f"/{key}/strategy_item", ["Strategy Item"]),
    (livee, f"/{key}/live", ["Live"]),
    (back, f"/{key}/back", ["Back"]),
]
for router, prefix, tags in routes : app.include_router(router, prefix=prefix, tags=tags)

#--------------------------------------------------------------------------------- Run
if __name__ == "__main__" : 
    uvicorn.run(app, host=host, port=port, log_level="info")