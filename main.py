# main.py

from fastapi import FastAPI
from movies.views import router as movies_router
from base.db_connection import create_db_and_tables

app = FastAPI()

app.include_router(movies_router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def root():
    return {"message": "Hello World"}
