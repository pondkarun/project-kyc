def extract_kyc_ocr(folder_id: str) -> dict:
    import easyocr
    import cv2
    import os
    import re

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
    # print("OCR Result:", result)
    for detection in result:
        text = detection[1].strip()
        
        # ID Number (Format: XXXX XXXXX XX)
        if extracted_data['id_number'] is None and re.match(r'^\d{4} \d{5} \d{2}$', text):
            extracted_data['id_number'] = text

        # Thai Name (Contains นาย / นาง / น.ส.)
        elif any(prefix in text for prefix in ['นาย', 'นาง', 'น.ส.']):
            if extracted_data['name_th'] is None:
                extracted_data['name_th'] = text
            else:
                extracted_data['name_th'] += ' ' + text

        # English Name (Starts with MR or looks like two English words)
        elif re.match(r'^(mr|mrs|ms)\s+[A-Za-z]+$', text.lower()):
            extracted_data['name_en'] = text
        elif re.match(r'^[A-Za-z]+$', text) and extracted_data['name_en']:
            extracted_data['name_en'] += ' ' + text

        # Thai Birth Date (e.g., 17 ก.ค. 2539)
        elif re.search(r'\d{1,2}\s+[ก-๙]+\.\s*\d{4}', text):
            extracted_data['birth_th'] = text

        # English Birth Date (e.g., Jul. 1996 or July 1996)
        elif re.search(r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+\d{4}', text.lower()):
            extracted_data['birth_en'] = text

        # Issue Date TH (e.g., 1 ก.พ. 2563)
        elif re.search(r'^\d+[ก-๙]+\.\s*\d{4}', text) and extracted_data['issue_th'] is None:
            extracted_data['issue_th'] = text

        # Expiry Date TH (มีปี พ.ศ. 257x)
        elif re.search(r'25[7-9]\d', text):
            extracted_data['expiry_th'] = text
    
    return extracted_data
