# 📄 app/workers/main.py
from fastapi import FastAPI
from app.api import process

app = FastAPI()
app.include_router(process.router, prefix="/process")