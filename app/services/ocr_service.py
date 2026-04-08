from typing import Dict
import os
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
import easyocr
import numpy as np
from PIL import Image

_reader = None


def get_easyocr_reader():
    global _reader
    if _reader is None:
        try:
            _reader = easyocr.Reader(["en"], gpu=True)
        except Exception:
            # Fallback to CPU if GPU not available
            _reader = easyocr.Reader(["en"], gpu=False)
    return _reader


def extract_ocr_data(image: Image.Image) -> Dict[str, float]:
    # Resize image for faster OCR processing
    max_size = 1024
    width, height = image.size
    if max(width, height) > max_size:
        ratio = max_size / max(width, height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    rgb_image = np.asarray(image.convert("RGB"))
    reader = get_easyocr_reader()
    results = reader.readtext(rgb_image, detail=1, paragraph=False)

    texts = [text for _, text, _ in results]
    confidences = [conf for _, _, conf in results]
    word_count = sum(len(text.split()) for text in texts)
    average_confidence = float(np.mean(confidences)) if confidences else 0.0
    full_text = " ".join(texts).strip()
    text_density = compute_text_density(image, results)

    return {
        "word_count": int(word_count),
        "average_confidence": average_confidence,
        "full_text": full_text,
        "text_density": float(text_density),
    }


def compute_text_density(image: Image.Image, ocr_results) -> float:
    width, height = image.size
    total_area = width * height
    if total_area == 0 or not ocr_results:
        return 0.0
    total_text_area = 0
    for box, _, _ in ocr_results:
        xs = [int(p[0]) for p in box]
        ys = [int(p[1]) for p in box]
        total_text_area += max(0, max(xs) - min(xs)) * max(0, max(ys) - min(ys))
    return float(min(1.0, total_text_area / total_area))
