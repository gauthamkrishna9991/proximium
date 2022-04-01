from fastapi import FastAPI

from proximium.api import api_router

app = FastAPI(title="Proximium")

app.include_router(api_router)
