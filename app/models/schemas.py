from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class ValidationResult(BaseModel):
    valid: bool
    error: Optional[str] = None

class FraudReport(BaseModel):
    document_name: str
    risk_level: str
    confidence: float
    findings: List[str]
    recommended_actions: List[str]
    details: Dict[str, Any]
