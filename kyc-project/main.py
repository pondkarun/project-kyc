import cv2
import easyocr
import re
import json
import os

# ---------- เตรียม Path ----------
img_path = 'images/id_card_pond.jpg'
output_img_path = 'outputs/id_card_with_ocr.jpg'
output_json_path = 'outputs/kyc_data.json'
os.makedirs("outputs", exist_ok=True)

# ---------- โหลด OCR Reader ----------
reader = easyocr.Reader(['th', 'en'], gpu=False)

# ---------- โหลดภาพ ----------
image = cv2.imread(img_path)
if image is None:
    print(f"❌ ไม่พบภาพที่: {img_path}")
    exit()

image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# ---------- OCR ----------
results = reader.readtext(image_rgb)

# ---------- วาดกรอบ OCR ลงภาพ ----------
for (bbox, text, conf) in results:
    pts = [tuple(map(int, point)) for point in bbox]
    cv2.rectangle(image, pts[0], pts[2], (0, 255, 0), 2)
    cv2.putText(image, text, pts[0], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

cv2.imwrite(output_img_path, image)
print(f"✅ บันทึกภาพพร้อมกรอบ OCR ที่: {output_img_path}")

# ---------- เตรียมข้อมูล ----------
texts = [text.lower().strip() for _, text, _ in results]
joined_text = ' '.join(texts)

kyc_data = {
    "id_number": None,
    "name_th": None,
    "name_en": None,
    "birth_th": None,
    "birth_en": None,
    "issue_th": None,
    "issue_en": None,
    "expiry_th": None,
    "expiry_en": None
}

# ---------- จับเลขบัตรประชาชน ----------
match = re.search(r'\d\s?\d{4}\s?\d{5}\s?\d{2}\s?\d', joined_text)
if match:
    kyc_data["id_number"] = match.group().replace(' ', '')

# ---------- จับชื่อไทย ----------
for t in texts:
    if 'ชื่อตัวและชื่อสกุล' in t:
        name_th = t.split('ชื่อตัวและชื่อสกุล')[-1].strip()
        kyc_data["name_th"] = name_th.replace('ฺ', '')  # ล้างสระเกิน
        break

# ---------- จับชื่ออังกฤษ (ชื่อ + นามสกุล จากบรรทัดถัดไป) ----------
for i, t in enumerate(texts):
    if 'mr.' in t:
        kyc_data["name_en"] = t.replace('mr.', '').strip().title()
    if 'last name' in t and i + 1 < len(texts):
        last = texts[i + 1].strip().title()
        if kyc_data["name_en"]:
            kyc_data["name_en"] += f' {last}'

# ---------- จับวันเกิด / วันออก / วันหมดอายุ จากบรรทัดถัดไป ----------
for i, t in enumerate(texts):
    if 'เกิดวันที่' in t and i + 1 < len(texts):
        kyc_data["birth_th"] = texts[i + 1].strip()
    elif 'date of birth' in t and i + 1 < len(texts):
        kyc_data["birth_en"] = texts[i + 1].strip().title()
    elif 'วันออกบัตร' in t and i + 1 < len(texts):
        kyc_data["issue_th"] = texts[i + 1].strip()
    elif 'date of issue' in t and i + 1 < len(texts):
        kyc_data["issue_en"] = texts[i + 1].strip().title()
    elif 'วันหมดอายุ' in t and i + 1 < len(texts):
        kyc_data["expiry_th"] = texts[i + 1].strip()
    elif 'date of expiry' in t and i + 1 < len(texts):
        kyc_data["expiry_en"] = texts[i + 1].strip().title()

# ---------- แสดงผล ----------
print("\n🎯 ข้อมูลที่แยกได้:")
for key, value in kyc_data.items():
    print(f"{key}: {value}")

# ---------- บันทึก JSON ----------
with open(output_json_path, "w", encoding="utf-8") as f:
    json.dump(kyc_data, f, ensure_ascii=False, indent=2)

print(f"\n✅ บันทึกผลลัพธ์ที่: {output_json_path}")