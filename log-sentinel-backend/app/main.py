from fastapi import FastAPI
from app.api.routes import router as api_router
from app.db.session import create_db_and_tables

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    create_db_and_tables()

app.include_router(api_router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to Log Sentinel API"}