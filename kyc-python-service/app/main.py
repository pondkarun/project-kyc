from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import models

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # ✅ อนุญาตทุก origin
    allow_credentials=False,  # ❌ ต้องเป็น False ถ้าใช้ "*"
    allow_methods=["*"],      # ✅ อนุญาตทุก method เช่น GET, POST, PUT
    allow_headers=["*"],      # ✅ อนุญาตทุก header
)

# สำหรับรับข้อมูลผ่าน POST
class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True

# Route ทดสอบ
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

@app.get("/kyc")
def list_kyc_requests(db: Session = FastAPI(get_db)):
    return db.query(models.KYCRequest).all()