FROM python:3.10-slim

# ติดตั้ง dependencies ที่จำเป็นสำหรับ face_recognition และ dlib
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libboost-all-dev \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    libatlas-base-dev \
    libjpeg-dev \
    libbz2-dev \
    libtiff-dev \
    libpng-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# ตั้ง working directory
WORKDIR /app

# คัดลอก requirements และติดตั้ง
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# คัดลอก source code ทั้งหมด
COPY . .

# รัน Python script ที่สั่ง uvicorn
CMD ["python", "run.py"]