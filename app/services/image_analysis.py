from typing import Dict, Any
import cv2
import numpy as np
from PIL import Image
from app.services.ocr_service import extract_ocr_data


def collect_image_metrics(image: Image.Image) -> Dict[str, Any]:
    cv_image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    ocr_data = extract_ocr_data(image)

    metrics = {
        "width": image.width,
        "height": image.height,
        "channels": int(cv_image.shape[2]) if cv_image.ndim == 3 else 1,
        "brightness": float(np.mean(gray) / 255.0),
        "contrast": float(np.std(gray) / 255.0),
        "edge_density": float(compute_edge_density(gray)),
        "blur_score": float(compute_blur_score(gray)),
        "noise_score": float(estimate_noise(gray)),
        "color_uniformity": float(color_uniformity(cv_image)),
        "palette_size": int(estimate_palette_size(cv_image)),
        "structure_score": float(estimate_structure_score(gray)),
        "ocr_word_count": int(ocr_data["word_count"]),
        "ocr_confidence": float(ocr_data["average_confidence"]),
        "ocr_text_density": float(ocr_data["text_density"]),
        "ocr_text": ocr_data["full_text"],
    }
    return metrics


def compute_edge_density(gray: np.ndarray) -> float:
    edges = cv2.Canny((gray).astype(np.uint8), 100, 200)
    return float(np.count_nonzero(edges) / max(1, edges.size))


def compute_blur_score(gray: np.ndarray) -> float:
    variance = cv2.Laplacian(gray, cv2.CV_64F).var()
    return float(min(1.0, variance / 200.0))


def estimate_noise(gray: np.ndarray) -> float:
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    diff = np.abs(gray.astype(np.int16) - blurred.astype(np.int16))
    return float(min(1.0, np.mean(diff) / 64.0))


def color_uniformity(image: np.ndarray) -> float:
    channels = cv2.split(image)
    hist_size = 16
    uniformity = 0.0
    for channel in channels:
        hist = cv2.calcHist([channel], [0], None, [hist_size], [0, 256])
        hist = hist.flatten()
        total = hist.sum() or 1
        uniformity += float(np.max(hist) / total)
    return float(min(1.0, uniformity / len(channels)))


def estimate_palette_size(image: np.ndarray) -> int:
    small = cv2.resize(image, (64, 64), interpolation=cv2.INTER_AREA)
    pixels = small.reshape(-1, 3)
    unique_colors = np.unique(pixels, axis=0)
    return int(min(unique_colors.shape[0], 256))


def estimate_structure_score(gray: np.ndarray) -> float:
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256]).flatten()
    total = hist.sum()
    if total == 0:
        return 0.0
    distribution = hist / total
    distribution = distribution[distribution > 0]
    entropy = -np.sum(distribution * np.log2(distribution))
    return float(min(1.0, entropy / 8.0))
