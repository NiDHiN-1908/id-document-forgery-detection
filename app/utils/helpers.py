from io import BytesIO
from PIL import Image


def safe_image_open(data) -> Image.Image:
    if hasattr(data, "seek"):
        data.seek(0)
    image = Image.open(data)
    image.verify()
    if hasattr(data, "seek"):
        data.seek(0)
    return image
