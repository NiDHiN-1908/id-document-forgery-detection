from typing import Dict, List, Tuple, Any
from app.models.schemas import FraudReport


def build_report(document_name: str, metrics: Dict[str, Any]) -> FraudReport:
    score, findings = score_metrics(metrics)
    risk_level = classify_risk(score)
    confidence = float(min(0.98, max(0.45, 0.5 + score * 0.5)))
    recommended_actions = generate_recommendations(risk_level)
    return FraudReport(
        document_name=document_name,
        risk_level=risk_level,
        confidence=round(confidence, 2),
        findings=findings,
        recommended_actions=recommended_actions,
        details=metrics,
    )


def score_metrics(metrics: Dict[str, Any]) -> Tuple[float, List[str]]:
    findings: List[str] = []
    score = 0.0
    if metrics.get("noise_score", 0) > 0.55:
        findings.append("High local noise and compression artifacts suggest the image may have been edited.")
        score += 0.20
    if metrics.get("blur_score", 0) < 0.22:
        findings.append("Image blur is low, which may indicate smoothing or resampling.")
        score += 0.18
    if metrics.get("color_uniformity", 0) > 0.62:
        findings.append("Large uniform color regions may indicate copy/paste or patching.")
        score += 0.15
    if metrics.get("palette_size", 0) < 12:
        findings.append("Low color variety can result from aggressive recompression or synthetic composition.")
        score += 0.12
    if metrics.get("edge_density", 0) < 0.08:
        findings.append("Weak edge detail may indicate smoothing or removal of printed text.")
        score += 0.18
    if metrics.get("structure_score", 0) < 0.35:
        findings.append("Low structure entropy suggests flattened or overly uniform document regions.")
        score += 0.15
    if metrics.get("ocr_text_density", 0) < 0.03:
        findings.append("Very little detected text may indicate a non-document or a heavily altered document.")
        score += 0.18
    if metrics.get("ocr_word_count", 0) < 8:
        findings.append("The OCR result includes few text tokens, which is unusual for a valid ID document.")
        score += 0.22
    if metrics.get("ocr_confidence", 0) < 0.45:
        findings.append("OCR confidence is low, suggesting the text could be distorted or tampered.")
        score += 0.18

    text_sample = str(metrics.get("ocr_text", "")).lower()
    expected_keywords = ["name", "id", "dob", "birth", "number", "passport", "license"]
    if text_sample and not any(keyword in text_sample for keyword in expected_keywords):
        findings.append("OCR did not detect expected document keywords such as name, ID, or DOB.")
        score += 0.12
    if not text_sample:
        findings.append("OCR did not detect any readable text in the document.")
        score += 0.25

    if score > 1.0:
        score = 1.0
    if not findings:
        findings.append("No strong forgery indicators were detected. Document appears visually consistent.")
    return score, findings


def classify_risk(score: float) -> str:
    if score >= 0.6:
        return "High"
    if score >= 0.3:
        return "Moderate"
    return "Low"


def generate_recommendations(risk_level: str) -> List[str]:
    if risk_level == "High":
        return [
            "Request a second image under different lighting conditions.",
            "Perform manual inspection and compare against known document templates.",
            "Verify the document data against authoritative identity sources.",
        ]
    if risk_level == "Moderate":
        return [
            "Ask the user for a second verification image.",
            "Review the document for visible discrepancies or alignment issues.",
            "Cross-check extracted text against known record fields.",
        ]
    return [
        "Proceed with standard identity verification steps.",
        "Monitor the transaction for additional fraud signals.",
    ]
