import json
import os
from uuid import UUID
from sqlalchemy.orm import Session
from app.db.models import KYCRequest
from app.utils.image_downloader import download_image_to_kyc_folder
from app.workers.detect_id_face_crop import detect_id_face_crop
from app.workers.extract_kyc_ocr import extract_kyc_ocr
from app.workers.kyc_check import run_kyc_check

FACE_MATCH_THRESHOLD = 85

print("ทำการโหลดโมดูล KYC Processor")

def process_kyc(db: Session, kyc_id: UUID):
    print("KYC Started processing...")
    kyc_record = db.query(KYCRequest).filter(KYCRequest.kyc_id == kyc_id).first()
    if not kyc_record:
        print(f"❌ KYC ID not found: {kyc_id}")
        return

    images = kyc_record.images or {}
    face_path = download_image_to_kyc_folder(images.get("face"), kyc_id, "face.jpg")
    id_front_path = download_image_to_kyc_folder(images.get("id_front"), kyc_id, "id_front.jpg")
    with_id_path = download_image_to_kyc_folder(images.get("with_id"), kyc_id, "with_id.jpg")

    print(f"Face path: {face_path}")
    print(f"ID front path: {id_front_path}")
    print(f"With ID path: {with_id_path}")

    if not all([face_path, id_front_path, with_id_path]):
        print(f"⚠️ Missing required images for KYC: {kyc_id}")
        return
    
    # result = {}
    detect_id_face_crop(kyc_id, "id_front.jpg")
    # result["data"] = extract_kyc_ocr(kyc_id)
    # result["kyc_data"] = run_kyc_check(kyc_id, FACE_MATCH_THRESHOLD)
    
    # kyc_record.result = result

    print("📦 Updating database...")
    kyc_record.status = "done"
    db.commit()

    print(f"✅ Done processing KYC: {kyc_id}")
