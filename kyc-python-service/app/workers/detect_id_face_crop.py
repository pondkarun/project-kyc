import cv2
from ultralytics import YOLO
import os

def detect_id_face_crop(folder_id: str, image_filename: str = "id_front.jpg"):
    image_path = f"temp/images/{folder_id}/{image_filename}"
    output_path = f"temp/images/{folder_id}/id_face_crop.jpg"
    model_path = "models/yolov8n.pt"
    os.makedirs(f"temp/images/{folder_id}", exist_ok=True)

    model = YOLO(model_path)

    image = cv2.imread(image_path)
    if image is None:
        raise Exception("❌ ไม่พบภาพบัตร")

    results = model(image)[0]
    faces = results.boxes.xyxy.cpu().numpy()

    if len(faces) == 0:
        raise Exception("❌ ไม่พบใบหน้าบนบัตร")

    faces = sorted(faces, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]), reverse=True)
    x1, y1, x2, y2 = [int(coord) for coord in faces[0]]

    face_crop = image[y1:y2, x1:x2]
    cv2.imwrite(output_path, face_crop)
    return output_path