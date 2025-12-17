from enum import Enum
from typing import List
from pydantic import BaseModel
from datetime import datetime

# Outcome status of research validation.
class ValidationStatus(str, Enum):
    PASS = "pass"
    RETRY = "retry"
    HUMAN_REVIEW = "human_review"
    FAIL = "fail"

# An issue identified during research validation.
class ValidationIssue(BaseModel):
    level: str
    message: str
    related_section: str

# Result of validating research quality and completeness.
class ValidationResult(BaseModel):
    status: ValidationStatus
    issues: List[ValidationIssue]
    overall_confidence: float
    validated_at: datetime
