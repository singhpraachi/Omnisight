from typing import Literal

from pydantic import BaseModel, Field


class SuggestedFix(BaseModel):
    type: Literal["css", "react"]
    code: str = Field(min_length=1, max_length=12000)
    rationale: str


class UIssue(BaseModel):
    element: str = Field(min_length=1)
    issue: str = Field(min_length=1)
    severity: Literal["low", "medium", "high", "critical"]
    evidence: str
    suggested_fix: SuggestedFix
    confidence: float = Field(ge=0.0, le=1.0)


class UIAuditReport(BaseModel):
    summary: str
    issues: list[UIssue]