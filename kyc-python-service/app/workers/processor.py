import json
import os
from uuid import UUID
from sqlalchemy.orm import Session
from app.db.models import KYCRequest
from app.workers.face_match import compare_faces_from_paths
from app.workers.ocr import extract_ocr_data
from app.core.config import settings

FACE_MATCH_THRESHOLD = 85.0

print("ทำการโหลดโมดูล KYC Processor")

def process_kyc(db: Session, kyc_id: UUID):
    print("KYC Started processing...")
    kyc_record = db.query(KYCRequest).filter(KYCRequest.kyc_id == kyc_id).first()
    if not kyc_record:
        print(f"❌ KYC ID not found: {kyc_id}")
        return

    images = kyc_record.images or {}
    base_url = settings.base_image_url.rstrip('/')
    face_path = f"{base_url}/{images.get('face')}" if images.get("face") else None
    id_front_path = f"{base_url}/{images.get('id_front')}" if images.get("id_front") else None
    with_id_path = f"{base_url}/{images.get('with_id')}" if images.get("with_id") else None

    if not all([face_path, id_front_path, with_id_path]):
        print(f"⚠️ Missing required images for KYC: {kyc_id}")
        return

    print("📥 Loading images...")
    try:
        score_face_with_id = compare_faces_from_paths(face_path, with_id_path, label="face vs with_id")
        score_face_idfront = compare_faces_from_paths(face_path, id_front_path, label="face vs id_front")
        score_with_id_idfront = compare_faces_from_paths(with_id_path, id_front_path, label="with_id vs id_front")
    except Exception as e:
        print(f"❌ Face matching error: {e}")
        return

    average_score = round((score_face_with_id + score_face_idfront + score_with_id_idfront) / 3, 2)
    passed = average_score >= FACE_MATCH_THRESHOLD

    print("🧠 Performing OCR on ID front...")
    try:
        ocr_result = extract_ocr_data(id_front_path)
    except Exception as e:
        print(f"❌ OCR error: {e}")
        ocr_result = {}

    print("📦 Updating database...")
    kyc_record.status = "done"
    kyc_record.result = {
        "face_scores": {
            "face_vs_with_id": round(score_face_with_id, 2),
            "face_vs_id_front": round(score_face_idfront, 2),
            "with_id_vs_id_front": round(score_with_id_idfront, 2),
            "average": average_score
        },
        "ocr": ocr_result,
        "passed": passed
    }
    db.commit()

    print(f"✅ Done processing KYC: {kyc_id}")
