import argparse
from pathlib import Path
import requests


API_URL = "http://127.0.0.1:8000/api/analyze"


def upload_document(image_path: Path, endpoint: str = API_URL) -> dict:
    if not image_path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    suffix = image_path.suffix.lower()
    if suffix == ".png":
        content_type = "image/png"
    elif suffix in {".jpg", ".jpeg"}:
        content_type = "image/jpeg"
    else:
        raise ValueError("Unsupported image format. Please use PNG or JPEG.")

    with open(image_path, "rb") as image_file:
        response = requests.post(
            endpoint,
            files={"file": (image_path.name, image_file, content_type)},
            timeout=30,
        )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload an ID document to the forgery detector API.")
    parser.add_argument("image_path", type=Path, help="Path to the ID image file")
    parser.add_argument("--url", type=str, default=API_URL, help="API endpoint URL")
    args = parser.parse_args()
    report = upload_document(args.image_path, args.url)
    print("Fraud Risk Report")
    print("===================")
    print(f"Document: {report['document_name']}")
    print(f"Risk level: {report['risk_level']} ({report['confidence']*100:.0f}%)")
    print("Findings:")
    for finding in report["findings"]:
        print(f"- {finding}")
    print("\nRecommended actions:")
    for action in report["recommended_actions"]:
        print(f"- {action}")
