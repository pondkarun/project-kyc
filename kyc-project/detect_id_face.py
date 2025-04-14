import cv2
from ultralytics import YOLO
import os

# ---------- config ----------
image_path = "images/id_card_pond.jpg"
output_path = "outputs/id_face_crop.jpg"
model_path = "models/yolov8n.pt"
os.makedirs("outputs", exist_ok=True)

# ---------- โหลดโมเดล ----------

model = YOLO(model_path)

# ---------- โหลดภาพ ----------
image = cv2.imread(image_path)
if image is None:
    print("❌ ไม่พบภาพบัตร")
    exit()

# ---------- ตรวจจับใบหน้า ----------
results = model(image)[0]
faces = results.boxes.xyxy.cpu().numpy()

if len(faces) == 0:
    print("❌ ไม่พบใบหน้าบนบัตร")
    exit()

# ---------- เลือกเฉพาะกรอบที่ใหญ่สุด (กรณีเจอหลายอัน) ----------
faces = sorted(faces, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]), reverse=True)
x1, y1, x2, y2 = [int(coord) for coord in faces[0]]

# ---------- crop ----------
face_crop = image[y1:y2, x1:x2]
cv2.imwrite(output_path, face_crop)
print(f"✅ ตัดใบหน้าจากบัตรเรียบร้อย → {output_path}")