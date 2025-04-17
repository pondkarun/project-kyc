# 1. ใช้ base image ที่เบาและรองรับได้ทุก lib
FROM python:3.10-slim

# 2. ตั้ง working directory
WORKDIR /app

# 3. ติดตั้ง system dependency พื้นฐาน
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    ffmpeg \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy project files
COPY . .

# 5. ติดตั้ง Python dependency
RUN pip install --upgrade pip

# ถ้าใช้ environment.yml:
# RUN pip install poetry
# RUN poetry install --no-dev

# หรือใช้ requirements.txt
# (สมมติว่าคุณ export requirements.txt ไว้แล้ว)
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# ถ้าไม่มี requirements.txt ใช้ pip install แบบตรงๆ ก็ได้ เช่น
# RUN pip install ultralytics fastapi pydantic sqlalchemy easyocr face_recognition opencv-python

# 6. เปิด port
EXPOSE 4000

# 7. คำสั่งรัน FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "4000"]