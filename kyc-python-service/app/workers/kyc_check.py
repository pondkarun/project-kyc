import json
import os
from PIL import Image
import numpy as np
import face_recognition

def load_rgb_image(path):
    print(f"📂 Loading image from: {path}")
    with Image.open(path) as img:
        img = img.convert("RGB")
        temp_path = "/tmp/kyc_temp.jpg"
        img.save(temp_path, format="JPEG")
        with Image.open(temp_path) as clean_img:
            rgb_img = np.asarray(clean_img, dtype=np.uint8)
            print(f"✅ Reloaded from temp: shape={rgb_img.shape}, dtype={rgb_img.dtype}")
            return rgb_img
    
def run_kyc_check(kyc_id: str, face_threshold: float) -> dict:
    # ---------- 2. โหลดภาพและเปรียบเทียบใบหน้า ----------
    try:
        img_id = load_rgb_image(f"temp/images/{kyc_id}/id_face_crop.jpg")
        assert img_id.ndim == 3 and img_id.shape[2] == 3, "ภาพ img_id ไม่ใช่ RGB"
        
        img_selfie = load_rgb_image(f"temp/images/{kyc_id}/face.jpg")
        assert img_selfie.ndim == 3 and img_selfie.shape[2] == 3, "ภาพ img_selfie ไม่ใช่ RGB"
        
        img_with_id = load_rgb_image(f"temp/images/{kyc_id}/with_id.jpg")
        assert img_with_id.ndim == 3 and img_with_id.shape[2] == 3, "ภาพ img_with_id ไม่ใช่ RGB"
    except Exception as e:
        raise RuntimeError(f"❌ ไม่สามารถโหลดรูปภาพได้: {e}")

    def get_encoding(image, label="unknown"):
        print(f"🔎 Encoding {label} | type: {type(image)}, shape: {image.shape}, dtype: {image.dtype}")
        
        # 🔥 Force to C-contiguous array
        image = np.ascontiguousarray(image, dtype=np.uint8)
        
        encodings = face_recognition.face_encodings(image)
        print(f"🔍 {label}: Found {len(encodings)} face(s)")
        if len(encodings) == 0:
            print(f"❌ ไม่พบใบหน้าใน: {label}")
            return None
        return encodings[0]

    def compare_faces(known, test, label="ไม่ระบุ"):
        if known is None or test is None:
            return 0
        distance = face_recognition.face_distance([known], test)[0]
        similarity = max(0, (1 - distance)) * 100
        return similarity

    enc_id = get_encoding(img_id, "บัตร")
    enc_selfie = get_encoding(img_selfie, "selfie")
    enc_with_id = get_encoding(img_with_id, "ถือบัตร")

    score_id_selfie = compare_faces(enc_id, enc_selfie, "ID ↔ Selfie")
    score_id_with = compare_faces(enc_id, enc_with_id, "ID ↔ ถือบัตร")
    score_selfie_with = compare_faces(enc_selfie, enc_with_id, "Selfie ↔ ถือบัตร")

    face_avg = round((score_id_selfie + score_id_with + score_selfie_with) / 3, 2)

    # ---------- 3. ตัดสินว่า ผ่าน KYC หรือไม่ ----------
    kyc_passed = face_avg >= face_threshold

    # ---------- 4. รวมข้อมูลและบันทึก ----------
    kyc_result = {
        "face_scores": {
            "id_vs_selfie": round(score_id_selfie, 2),
            "id_vs_with_id": round(score_id_with, 2),
            "selfie_vs_with_id": round(score_selfie_with, 2),
            "average": face_avg
        },
        "kyc_passed": kyc_passed
    }

    return kyc_result