import json
import os
import face_recognition

def get_encoding(image, label="unknown"):
    encodings = face_recognition.face_encodings(image)
    if len(encodings) == 0:
        print(f"❌ ไม่พบใบหน้าใน: {label}")
        return None
    return encodings[0]

def compare_faces(known, test, label="ไม่ระบุ"):
    if known is None or test is None:
        print(f"⚠️ ไม่สามารถเปรียบเทียบ {label} ได้")
        return 0
    distance = face_recognition.face_distance([known], test)[0]
    similarity = max(0, (1 - distance)) * 100
    print(f"✅ ความคล้ายใบหน้า {label}: {similarity:.2f}%")
    return similarity

def process_kyc_check(kyc_id: str, face_threshold: float = 85) -> dict:
    base_path = f"temp/images/{kyc_id}"
    img_id = face_recognition.load_image_file(os.path.join(base_path, "id_face_crop.jpg"))
    img_selfie = face_recognition.load_image_file(os.path.join(base_path, "face.jpg"))
    img_with_id = face_recognition.load_image_file(os.path.join(base_path, "with_id.jpg"))

    enc_id = get_encoding(img_id, "บัตร")
    enc_selfie = get_encoding(img_selfie, "selfie")
    enc_with_id = get_encoding(img_with_id, "ถือบัตร")

    score_id_selfie = compare_faces(enc_id, enc_selfie, "ID ↔ Selfie")
    score_id_with = compare_faces(enc_id, enc_with_id, "ID ↔ ถือบัตร")
    score_selfie_with = compare_faces(enc_selfie, enc_with_id, "Selfie ↔ ถือบัตร")

    face_avg = round((score_id_selfie + score_id_with + score_selfie_with) / 3, 2)

    kyc_passed = bool(face_avg >= face_threshold)

    result = {
        "face_scores": {
            "id_vs_selfie": round(score_id_selfie, 2),
            "id_vs_with_id": round(score_id_with, 2),
            "selfie_vs_with_id": round(score_selfie_with, 2),
            "average": face_avg
        },
        "kyc_passed": kyc_passed
    }

    print(f"✅ KYC Check Result: {result}")
    return result