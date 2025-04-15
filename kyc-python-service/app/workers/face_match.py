import face_recognition
import numpy as np
import requests
from PIL import Image
from io import BytesIO
import os

def load_image(image_path: str):
    if image_path.startswith("http"):
        response = requests.get(image_path)
        image = Image.open(BytesIO(response.content)).convert("RGB")
        return np.array(image)
    else:
        return face_recognition.load_image_file(image_path)

def get_face_encoding(image):
    encodings = face_recognition.face_encodings(image)
    return encodings[0] if encodings else None

def compare_faces_from_paths(img_path1: str, img_path2: str, label: str = "") -> float:
    try:
        img1 = load_image(img_path1)
        img2 = load_image(img_path2)

        enc1 = get_face_encoding(img1)
        enc2 = get_face_encoding(img2)

        if enc1 is None or enc2 is None:
            print(f"❌ ไม่พบใบหน้าในภาพ ({label})")
            return 0.0

        distance = face_recognition.face_distance([enc1], enc2)[0]
        similarity = max(0.0, (1 - distance) * 100)
        print(f"✅ ความคล้ายใบหน้า {label}: {similarity:.2f}%")
        return round(similarity, 2)

    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในการเปรียบเทียบ ({label}): {e}")
        return 0.0
