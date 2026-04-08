import io
from pathlib import Path
from fastapi.testclient import TestClient
from PIL import Image
from app.main import app

client = TestClient(app)


def create_test_image() -> io.BytesIO:
    image = Image.new("RGB", (560, 360), color=(220, 220, 220))
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


def test_root_page_contains_upload_form():
    response = client.get("/")
    assert response.status_code == 200
    assert "Upload ID Document" in response.text


def test_api_analyze_accepts_valid_image():
    test_image = create_test_image()
    response = client.post(
        "/api/analyze",
        files={"file": ("test_id.png", test_image, "image/png")},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["document_name"] == "test_id.png"
    assert payload["risk_level"] in {"Low", "Moderate", "High"}
    assert isinstance(payload["findings"], list)
    assert "details" in payload
    assert "ocr_word_count" in payload["details"]
    assert "ocr_confidence" in payload["details"]
    assert "ocr_text" in payload["details"]


def test_api_rejects_invalid_mime_type():
    response = client.post(
        "/api/analyze",
        files={"file": ("malware.jpg", b"not an image", "text/plain")},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Unsupported image MIME type."
