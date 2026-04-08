import os
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

from fastapi import FastAPI
from app.routes.analyze import router as analyze_router

app = FastAPI(
    title="ID Forgery Detector",
    description="Prototype service to analyze ID images and generate a forgery risk report.",
)

app.include_router(analyze_router)
