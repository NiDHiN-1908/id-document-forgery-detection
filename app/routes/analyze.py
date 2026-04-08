from pathlib import Path
from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.schemas import FraudReport
from app.services.fraud_engine import analyze_image_and_generate_report, validate_image_file

TEMPLATES_DIRECTORY = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIRECTORY))

router = APIRouter(tags=["analysis"])

@router.get("/", response_class=HTMLResponse)
def upload_form(request: Request):
    """Render the document upload form."""
    return templates.TemplateResponse(request, "upload.html", {"request": request, "error": None})

@router.post("/analyze", response_class=HTMLResponse)
async def analyze_document(request: Request, file: UploadFile = File(...)):
    """Analyze an uploaded document image and render the report page."""
    validation = validate_image_file(file)
    if not validation.valid:
        return templates.TemplateResponse(request, "upload.html", {"request": request, "error": validation.error})

    content = await file.read()
    report = analyze_image_and_generate_report(content, file.filename)

    return templates.TemplateResponse(
        request,
        "report.html",
        {
            "request": request,
            "report": report.dict(),
            "json_report": report.model_dump_json(indent=2),
        },
    )

@router.post("/api/analyze", response_model=FraudReport)
async def analyze_document_api(file: UploadFile = File(...)):
    """Analyze an uploaded document image and return the JSON report."""
    validation = validate_image_file(file)
    if not validation.valid:
        raise HTTPException(status_code=400, detail=validation.error)

    content = await file.read()
    return analyze_image_and_generate_report(content, file.filename)
