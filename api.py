#--------------------------------------------------------------------------------- location
# webapi.py

#--------------------------------------------------------------------------------- Description
# This is main file of webapi

#--------------------------------------------------------------------------------- Import
import uvicorn
from myLib.utils import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from webapi import *

#--------------------------------------------------------------------------------- Variable
title = config.get("api", {}).get("title", {})
description = config.get("api", {}).get("description", {})
version = config.get("api", {}).get("version", {})
openapi_url = config.get("api", {}).get("openapi_url", {})
docs_url = config.get("api", {}).get("docs_url", {})
redoc_url = config.get("api", {}).get("redoc_url", {})
key = config.get("api", {}).get("key", {})
host = config.get("api", {}).get("host", {})
port = config.get("api", {}).get("port", {})

#--------------------------------------------------------------------------------- App
app = FastAPI(
    title = title,
    description = description,
    version=version,
    openapi_url=openapi_url,
    docs_url=docs_url,
    redoc_url=redoc_url,
    root_path=f"/"
)
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"]
) 

#--------------------------------------------------------------------------------- Route
routes = [
    (account, "/account", ["Account"]),
    (instrument, "/instrument", ["Instrument"]),
    (strategy, "/strategy", ["Strategy"]),
    (strategy_item, "/strategy_item", ["Strategy Item"]),
    (live_execute, "/live_execute", ["Live Execute"]),
    (live_order, "/live_order", ["Live Order"]),
]
for router, prefix, tags in routes : app.include_router(router, prefix=prefix, tags=tags)

#--------------------------------------------------------------------------------- Run
if __name__ == "__main__" : uvicorn.run(app, host=host, port=port)