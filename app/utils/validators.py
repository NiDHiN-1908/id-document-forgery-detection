from pathlib import Path

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png"}


def is_allowed_extension(filename: str) -> bool:
    return Path(filename or "").suffix.lower() in ALLOWED_EXTENSIONS


def is_image_content_type(content_type: str) -> bool:
    return (content_type or "").lower() in ALLOWED_MIME_TYPES
