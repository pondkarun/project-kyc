from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine
engine = create_engine(DATABASE_URL)

# SessionLocal คือคลาสสำหรับสร้าง session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base สำหรับใช้ inherit ตอนประกาศ model
Base = declarative_base()

# ✅ ฟังก์ชันนี้จะใช้ใน Depends() เพื่อให้ FastAPI สร้าง session/ปิดอัตโนมัติ
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()