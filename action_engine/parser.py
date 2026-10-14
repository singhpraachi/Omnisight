import json
from typing import Any

from pydantic import ValidationError

from action_engine.models import UIAuditReport


class ActionEngineError(ValueError):
    """Raised when a VLM report cannot be processed."""


def parse_audit_report(
    report: str | dict[str, Any] | UIAuditReport,
) -> UIAuditReport:
    """Parse and validate a VLM report from JSON or a dictionary."""

    if isinstance(report, UIAuditReport):
        return report

    if isinstance(report, str):
        try:
            report = json.loads(report)
        except json.JSONDecodeError as exc:
            raise ActionEngineError(
                "The VLM report is not valid JSON."
            ) from exc

    if not isinstance(report, dict):
        raise ActionEngineError(
            "The VLM report must be a JSON object."
        )

    try:
        return UIAuditReport.model_validate(report)
    except ValidationError as exc:
        raise ActionEngineError(
            "The VLM report does not match the expected schema."
        ) from exc


def extract_fix_proposals(
    report: str | dict[str, Any] | UIAuditReport,
) -> list[dict[str, Any]]:
    """Extract proposed fixes without executing or applying them."""

    audit = parse_audit_report(report)
    proposals = []

    for item in audit.issues:
        proposals.append({
            "element": item.element,
            "issue": item.issue,
            "severity": item.severity,
            "evidence": item.evidence,
            "confidence": item.confidence,
            "fix_type": item.suggested_fix.type,
            "code": item.suggested_fix.code,
            "rationale": item.suggested_fix.rationale,
        })

    return proposals