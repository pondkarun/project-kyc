import os
import uuid
import requests
from pathlib import Path
from app.core.config import settings

TEMP_DIR = Path(__file__).resolve().parent.parent.parent / "temp/images"
os.makedirs(TEMP_DIR, exist_ok=True)

def download_image_to_temp(image_relative_url: str) -> str:
    full_url = f"{settings.base_image_url.rstrip('/')}/{image_relative_url.lstrip('/')}"
    filename = f"{uuid.uuid4().hex}.jpg"
    file_path = TEMP_DIR / filename

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
