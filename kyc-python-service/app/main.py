from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

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

# รับพารามิเตอร์จาก URL
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}

# POST endpoint รับข้อมูลจาก body
@app.post("/items/")
def create_item(item: Item):
    return {"received_item": item}