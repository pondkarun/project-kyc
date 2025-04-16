import json
import os
from uuid import UUID
from sqlalchemy.orm import Session
from app.db.models import KYCRequest
from app.workers.face_match import compare_faces_from_paths
from app.workers.ocr import extract_ocr_data
from app.utils.image_downloader import download_image_to_kyc_folder

FACE_MATCH_THRESHOLD = 85.0

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

    print(f"✅ Done processing KYC: {kyc_id}")
