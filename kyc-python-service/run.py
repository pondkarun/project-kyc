import os
from dotenv import load_dotenv
import uvicorn

# โหลดค่าจาก .env
load_dotenv()

# ดึง host และ port
host = os.getenv("HOST", "127.0.0.1")
port = int(os.getenv("PORT", 8000))

print("PORT from env:", os.getenv("PORT"))
print("port after int():", port)

# รัน uvicorn โดยชี้ไปที่ app.main:app
reload = os.getenv("RELOAD", "true").lower() == "true"
uvicorn.run("app.main:app", host=host, port=port, reload=reload)