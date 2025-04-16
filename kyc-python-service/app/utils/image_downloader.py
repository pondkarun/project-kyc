import os
import requests
from pathlib import Path
from app.core.config import settings

TEMP_DIR = Path(__file__).resolve().parent.parent.parent / "temp/images"
os.makedirs(TEMP_DIR, exist_ok=True)

def download_image_to_kyc_folder(image_relative_url: str, kyc_id: str, filename: str) -> str:
    full_url = f"{settings.base_image_url.rstrip('/')}/{image_relative_url.lstrip('/')}"
    kyc_folder = TEMP_DIR / str(kyc_id)

    # Ensure TEMP_DIR and kyc_folder exist
    os.makedirs(TEMP_DIR, exist_ok=True)
    os.makedirs(kyc_folder, exist_ok=True)

    file_path = kyc_folder / filename

    try:
        response = requests.get(full_url, timeout=10)
        response.raise_for_status()
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"✅ Downloaded: {full_url} -> {file_path}")
        return str(file_path)
    except Exception as e:
        print(f"❌ Failed to download {full_url}: {e}")
        return ""
