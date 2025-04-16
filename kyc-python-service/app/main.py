from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import models


from uuid import UUID
from fastapi import BackgroundTasks, HTTPException

from app.workers import processor

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
def list_kyc_requests(db: Session = Depends(get_db)):
    return db.query(models.KYCRequest).all()

@app.post("/kyc/process/{kyc_id}")
async def process_kyc(
    kyc_id: UUID,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    kyc_record = db.query(models.KYCRequest).filter(models.KYCRequest.kyc_id == kyc_id).first()
    if not kyc_record:
        raise HTTPException(status_code=404, detail="kyc_id not found")

    if kyc_record.status == "processed":
        raise HTTPException(status_code=400, detail="already processed")

    # เปลี่ยนสถานะเป็น processed ทันที
    kyc_record.status = "processed"
    db.commit()

    # background task
    background_tasks.add_task(processor.process_kyc, db, kyc_record)

    return {"message": "processing started"}