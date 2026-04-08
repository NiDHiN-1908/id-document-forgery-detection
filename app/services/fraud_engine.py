from io import BytesIO
from fastapi import UploadFile
from PIL import Image
from app.models.schemas import ValidationResult, FraudReport
from app.services.image_analysis import collect_image_metrics
from app.services.report_generator import build_report
from app.utils.helpers import safe_image_open
from app.utils.validators import is_allowed_extension, is_image_content_type


def validate_image_file(file: UploadFile) -> ValidationResult:
    if not is_allowed_extension(file.filename):
        return ValidationResult(valid=False, error="Unsupported file extension. Use JPG, JPEG, or PNG.")
    if not is_image_content_type(file.content_type):
        return ValidationResult(valid=False, error="Unsupported image MIME type.")
    try:
        file.file.seek(0)
        safe_image_open(file.file)
    except Exception:
        return ValidationResult(valid=False, error="Unable to parse the uploaded file as an image.")
    return ValidationResult(valid=True)


def analyze_image_and_generate_report(file_bytes: bytes, document_name: str) -> FraudReport:
    try:
        image = Image.open(BytesIO(file_bytes)).convert("RGB")
        metrics = collect_image_metrics(image)
        return build_report(document_name, metrics)
    except Exception as e:
        return FraudReport(
            document_name=document_name,
            risk_level="High",
            confidence=0.95,
            findings=["Unable to analyze image due to processing error."],
            recommended_actions=["Verify the image file is valid and try again."],
            details={"error": str(e)},
        )
