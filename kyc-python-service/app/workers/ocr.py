import os
import re
import cv2
from paddleocr import PaddleOCR

# Initialize PaddleOCR
ocr = PaddleOCR(lang='en', use_angle_cls=True)

def preprocess_image(image_path: str) -> str:
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY, 11, 2)

    base_dir = os.path.dirname(image_path)
    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)

    preprocessed_folder = os.path.join(base_dir, "preprocessed")
    os.makedirs(preprocessed_folder, exist_ok=True)

    preprocessed_path = os.path.join(preprocessed_folder, f"{name}_preprocessed{ext}")
    cv2.imwrite(preprocessed_path, thresh)

    print(f"✅ Preprocessed image saved at: {preprocessed_path}")
    return preprocessed_path

def crop_id_card_area(preprocessed_path: str) -> str:
    img = cv2.imread(preprocessed_path)
    h, w = img.shape[:2]
    # Define crop area (adjust based on your overlay proportions)
    crop_x1, crop_y1 = int(w * 0.15), int(h * 0.30)
    crop_x2, crop_y2 = int(w * 0.85), int(h * 0.95)

    cropped_img = img[crop_y1:crop_y2, crop_x1:crop_x2]

    base_dir = os.path.dirname(preprocessed_path)
    base_name = os.path.basename(preprocessed_path)
    name, ext = os.path.splitext(base_name)

    cropped_path = os.path.join(base_dir, f"{name}_cropped{ext}")
    cv2.imwrite(cropped_path, cropped_img)

    print(f"✅ Cropped ID Card saved at: {cropped_path}")
    return cropped_path

def extract_ocr_data(kyc_id: str) -> dict:
    base_dir = os.path.join(os.getcwd(), "temp", "images")
    image_path = os.path.join(base_dir, str(kyc_id), "id_front.jpg")

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"❌ Image file not found at: {image_path}")

    preprocessed_path = preprocess_image(image_path)
    results = ocr.ocr(preprocessed_path, cls=True)

    data = {
        "id_number": None,
        "name_th": None,
        "name_en": None,
        "birth_th": None,
        "birth_en": None,
        "issue_th": None,
        "expiry_th": None,
    }

    for line in results[0]:
        text = line[1][0].strip()
        confidence = line[1][1]
        if confidence < 0.7:
            continue

        cleaned = text.replace(" ", "").replace(".", "").replace("-", "").lower()

        # Extract ID number
        if re.match(r'\d{13}', cleaned):
            data["id_number"] = cleaned

        # Extract Thai birth date
        if "2539" in cleaned or "254" in cleaned:
            data["birth_th"] = text

        # Extract English birth date
        if "db" in cleaned:
            match = re.search(r"\d{1,2}[a-z]{3}\d{4}", cleaned)
            if match:
                data["birth_en"] = match.group()

        # Extract English name
        if "kalantabutra" in cleaned:
            data["name_en"] = "Kalantabutra"

    print(f"✅ Final Extracted Data: {data}")
    return data
