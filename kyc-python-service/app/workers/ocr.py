import easyocr

reader = easyocr.Reader(["th", "en"], gpu=False)

def extract_ocr_data(image_path: str) -> dict:
    results = reader.readtext(image_path)
    texts = [text.lower() for _, text, _ in results]

    data = {
        "id_number": None,
        "name_th": None,
        "birth_th": None,
        "birth_en": None,
    }

    joined_text = " ".join(texts)

    # ดึงเลขบัตรประชาชน (13 หลัก)
    import re
    match = re.search(r"\d{1}\s?\d{4}\s?\d{5}\s?\d{2}\s?\d{1}", joined_text)
    if match:
        data["id_number"] = match.group().replace(" ", "")

    # ดึงชื่อภาษาไทย
    for t in texts:
        if "ชื่อตัวและชื่อสกุล" in t:
            data["name_th"] = t.split("ชื่อตัวและชื่อสกุล")[-1].strip()
            break

    # ดึงวันเกิด
    for t in texts:
        if "เกิดวันที่" in t:
            data["birth_th"] = t.replace("เกิดวันที่", "").strip()
        elif "date of birth" in t:
            data["birth_en"] = t.replace("date of birth", "").strip()

    return data
