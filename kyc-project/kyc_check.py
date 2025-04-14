import json
import os
import face_recognition

# ---------- 1. โหลดข้อมูล OCR ----------
with open("outputs/kyc_data.json", "r", encoding="utf-8") as f:
    kyc_data = json.load(f)

# ---------- 2. โหลดภาพและเปรียบเทียบใบหน้า ----------
img_id = face_recognition.load_image_file("outputs/id_face_crop.jpg")
img_selfie = face_recognition.load_image_file("images/selfie_pond.jpg")
img_with_id = face_recognition.load_image_file("images/selfie_with_id_pond.jpg")

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

enc_id = get_encoding(img_id, "บัตร")
enc_selfie = get_encoding(img_selfie, "selfie")
enc_with_id = get_encoding(img_with_id, "ถือบัตร")

score_id_selfie = compare_faces(enc_id, enc_selfie, "ID ↔ Selfie")
score_id_with = compare_faces(enc_id, enc_with_id, "ID ↔ ถือบัตร")
score_selfie_with = compare_faces(enc_selfie, enc_with_id, "Selfie ↔ ถือบัตร")

face_avg = round((score_id_selfie + score_id_with + score_selfie_with) / 3, 2)

# ---------- 3. ตัดสินว่า ผ่าน KYC หรือไม่ ----------
face_threshold = 85  # เปอร์เซ็นต์ขั้นต่ำที่ต้องผ่าน
kyc_passed = bool(
    face_avg >= face_threshold and
    kyc_data.get("id_number") is not None and
    kyc_data.get("name_th") is not None
)

# ---------- 4. รวมข้อมูลและบันทึก ----------
kyc_data["face_scores"] = {
    "id_vs_selfie": round(score_id_selfie, 2),
    "id_vs_with_id": round(score_id_with, 2),
    "selfie_vs_with_id": round(score_selfie_with, 2),
    "average": face_avg
}
kyc_data["kyc_passed"] = kyc_passed

with open("outputs/kyc_result.json", "w", encoding="utf-8") as f:
    json.dump(kyc_data, f, ensure_ascii=False, indent=2)

print(f"\n🎯 สรุปผล KYC: {'ผ่าน ✅' if kyc_passed else 'ไม่ผ่าน ❌'}")
print("📄 บันทึกผลไว้ที่: outputs/kyc_result.json")