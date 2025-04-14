import face_recognition
import os

# โหลดภาพจากโฟลเดอร์
img_id = face_recognition.load_image_file("images/id_card_pond.jpg")
img_selfie = face_recognition.load_image_file("images/selfie_pond.jpg")
img_with_id = face_recognition.load_image_file("images/selfie_with_id_pond.jpg")

# ฟังก์ชันสำหรับดึง face encoding
def get_encoding(image, label="unknown"):
    encodings = face_recognition.face_encodings(image)
    if len(encodings) == 0:
        print(f"❌ ไม่พบใบหน้าใน: {label}")
        return None
    return encodings[0]

# ดึง encodings
enc_id = get_encoding(img_id, "บัตรประชาชน")
enc_selfie = get_encoding(img_selfie, "เซลฟี่")
enc_with_id = get_encoding(img_with_id, "ถือบัตร")

# ฟังก์ชันเปรียบเทียบใบหน้า
def compare_faces(known, test, label="ไม่ระบุ"):
    if known is None or test is None:
        print(f"⚠️ ไม่สามารถเปรียบเทียบ {label} ได้")
        return 0
    distance = face_recognition.face_distance([known], test)[0]
    similarity = max(0, (1 - distance)) * 100
    print(f"✅ ความคล้ายใบหน้า {label}: {similarity:.2f}%")
    return similarity

# เปรียบเทียบทั้ง 3 คู่
score1 = compare_faces(enc_id, enc_selfie, "ID ↔ Selfie")
score2 = compare_faces(enc_id, enc_with_id, "ID ↔ ถือบัตร")
score3 = compare_faces(enc_selfie, enc_with_id, "Selfie ↔ ถือบัตร")

# สรุปผล
avg_score = round((score1 + score2 + score3) / 3, 2)
print(f"\n🎯 ค่าเฉลี่ยความคล้ายของใบหน้า: {avg_score:.2f}%")