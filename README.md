# ID Forgery Detector

This prototype accepts an uploaded ID document image, validates the format, analyzes image characteristics for potential tampering, and generates a structured fraud risk report.

## Architecture

- `app/main.py` - FastAPI application entrypoint.
- `app/routes/analyze.py` - Upload page and analysis endpoints.
- `app/services/` - Image analysis, validation, and report generation logic.
- `app/models/schemas.py` - Report and validation data models.
- `app/templates/` - HTML pages for upload and report display.
- `frontend/app.py` - Simple CLI client to upload an image to the API.
- `tests/test_api.py` - API tests for upload and validation behavior.

## Key approach

- Validates file extension and MIME type for PNG/JPEG uploads.
- Uses image heuristics to inspect brightness, edge density, noise, color uniformity, palette size, structure entropy, and text-like density.
- Combines these signals into a risk score, providing a `Low`, `Moderate`, or `High` forgery risk classification.
- Generates a human-readable report with findings and recommended actions.

## Run locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the API:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
3. Open the browser at:
   ```text
   http://127.0.0.1:8000/
   ```

## Sample CLI usage

```bash
python frontend/app.py path/to/id_image.png
```

## Testing

Run tests with:

```bash
pytest tests/test_api.py
```

## Notes

- This is a prototype for document fraud analysis using heuristic image analysis.
- The focus is on problem understanding, structured reporting, and prototype delivery rather than production-grade biometric verification.
