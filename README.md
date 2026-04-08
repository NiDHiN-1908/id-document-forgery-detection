# ID Forgery Detector

A prototype FastAPI service for analyzing ID document images and generating a structured fraud risk report.

## Project overview

This repository implements a lightweight forgery detection workflow using image heuristics and OCR signals.

- `app/main.py` — FastAPI application entry point.
- `app/routes/analyze.py` — Web form and API endpoints for document analysis.
- `app/services/` — Image processing, OCR validation, and risk scoring logic.
- `app/models/schemas.py` — Pydantic models for validation and report payloads.
- `app/templates/` — Jinja2 views for upload and report rendering.
- `frontend/app.py` — CLI client to submit an image to the API.
- `tests/test_api.py` — Integration tests for the application endpoints.

## Features

- File validation for JPEG/PNG image uploads.
- Heuristic image analysis including brightness, contrast, edge density, noise, structure, and color uniformity.
- OCR inspection to verify text presence, keyword signals, confidence, and text density.
- Risk scoring engine that classifies documents as `Low`, `Moderate`, or `High` forgery risk.
- Human-readable findings and recommended next steps.
- Lightweight health endpoint for monitoring.

## Installation

1. Create and activate your Python environment.

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate    # Windows
   ```

2. Install dependencies.

   ```bash
   pip install -r requirements.txt
   ```

## Running locally

Start the API server:

```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open the browser at:

```text
http://127.0.0.1:8000/
```

The OpenAPI docs are available at:

```text
http://127.0.0.1:8000/docs
```

## CLI usage

Use the CLI client to submit an ID image to the API:

```bash
python frontend/app.py path/to/id_image.png
```

## Testing

Run the API test suite:

```bash
python -m pytest tests/test_api.py
```

## Notes

- This project is a prototype and should not replace a production identity verification system.
- For better runtime performance, use a GPU-capable environment or reduce OCR resolution.
- The app is designed for easy extension and can be integrated into a larger identity verification pipeline.
