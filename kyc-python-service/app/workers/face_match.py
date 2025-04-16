import cv2
import face_recognition
import numpy as np

def load_image(path: str) -> np.ndarray | None:
    try:
        image = cv2.imread(path)
        if image is None:
            print(f"❌ ไม่สามารถโหลดภาพจาก {path}")
            return None
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    except Exception as e:
        print(f"❌ Error loading image: {e}")
        return None

def get_face_encoding(image: np.ndarray) -> np.ndarray | None:
    try:
        encodings = face_recognition.face_encodings(image)
        return encodings[0] if encodings else None
    except Exception as e:
        print(f"❌ Error encoding face: {e}")
        return None

def compare_faces_from_paths(img_path1: str, img_path2: str, label: str = "", name1: str = "img1", name2: str = "img2") -> float:
    print(f"\n📥 Comparing: {name1} ↔ {name2} ({label})")

    img1 = load_image(img_path1)
    img2 = load_image(img_path2)

    if img1 is None or img2 is None:
        print(f"❌ โหลดภาพไม่สำเร็จ ({label})")
        return 0.0

    print(f"📏 ขนาดภาพ {label}: {img1.shape} / {img2.shape}")
    print(f"🧪 dtype: {img1.dtype} / {img2.dtype}")

    enc1 = get_face_encoding(img1)
    enc2 = get_face_encoding(img2)

    if enc1 is None or enc2 is None:
        print(f"❌ ไม่พบใบหน้าในภาพ ({label})")
        return 0.0

    distance = face_recognition.face_distance([enc1], enc2)[0]
    similarity = max(0.0, (1 - distance) * 100)
    print(f"✅ ความคล้ายใบหน้า {label} ({name1} ↔ {name2}): {similarity:.2f}%")
    return round(similarity, 2)
