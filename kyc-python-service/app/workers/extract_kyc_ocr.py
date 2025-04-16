def extract_kyc_ocr(folder_id: str) -> dict:
    import easyocr
    import cv2
    import os

    img_path = f'temp/images/{folder_id}/id_front.jpg'
    
    # Load the image
    image = cv2.imread(img_path)
    
    # Initialize EasyOCR Reader
    reader = easyocr.Reader(['en', 'th'])
    
    # Perform OCR
    result = reader.readtext(image)
    
    # Initialize a dictionary to hold the extracted data
    extracted_data = {
        'id_number': None,
        'name_th': None,
        'name_en': None,
        'birth_th': None,
        'birth_en': None,
        'issue_th': None,
        'issue_en': None,
        'expiry_th': None,
        'expiry_en': None
    }
    
    # Process the result to extract relevant fields
    for detection in result:
        text = detection[1]
        if 'id number' in text.lower():
            extracted_data['id_number'] = text.split(':')[-1].strip()
        elif 'name' in text.lower() and 'th' in text.lower():
            extracted_data['name_th'] = text.split(':')[-1].strip()
        elif 'name' in text.lower() and 'en' in text.lower():
            extracted_data['name_en'] = text.split(':')[-1].strip()
        elif 'birth' in text.lower() and 'th' in text.lower():
            extracted_data['birth_th'] = text.split(':')[-1].strip()
        elif 'birth' in text.lower() and 'en' in text.lower():
            extracted_data['birth_en'] = text.split(':')[-1].strip()
        elif 'issue' in text.lower() and 'th' in text.lower():
            extracted_data['issue_th'] = text.split(':')[-1].strip()
        elif 'issue' in text.lower() and 'en' in text.lower():
            extracted_data['issue_en'] = text.split(':')[-1].strip()
        elif 'expiry' in text.lower() and 'th' in text.lower():
            extracted_data['expiry_th'] = text.split(':')[-1].strip()
        elif 'expiry' in text.lower() and 'en' in text.lower():
            extracted_data['expiry_en'] = text.split(':')[-1].strip()
    
    return extracted_data
