
import re
from typing import Any

from action_engine.models import UIAuditReport
from action_engine.parser import ActionEngineError, parse_audit_report

CSS_BLOCKED_PATTERNS = [
    r"@import\b",
    r"expression\s*\(",
    r"javascript\s*:",
    r"<\s*script\b",
    r"</\s*style\s*>",
]

REACT_BLOCKED_PATTERNS = [
    r"\beval\s*\(",
    r"\bnew\s+Function\b",
    r"\bchild_process\b",
    r"\bprocess\.",
    r"\brequire\s*\(",
    r"\bimport\s*\(",
    r"\bdangerouslySetInnerHTML\b",
    r"<\s*script\b",
]

MAX_PROPOSALS = 100


def validate_fix_code(fix_type: str, code: str) -> tuple[bool, str]:
    """Perform basic checks on a proposed fix; human review is still required."""
    if fix_type not in {"css", "react"}:
        return False, "Unsupported fix type."

    if not isinstance(code, str) or not code.strip():
        return False, "Fix code must be a non-empty string."

    if len(code) > 12000:
        return False, "Fix code exceeds the maximum allowed length."

    patterns = (
        CSS_BLOCKED_PATTERNS
        if fix_type == "css"
        else REACT_BLOCKED_PATTERNS
    )

    for pattern in patterns:
        if re.search(pattern, code, flags=re.IGNORECASE):
            return False, f"Fix rejected due to a blocked {fix_type.upper()} pattern."

    if fix_type == "css" and ("{" not in code or "}" not in code):
        return False, "CSS proposal must contain a rule block."

    return True, "Passed basic checks; human review is still required."


def prepare_review_package(
    report: str | dict[str, Any] | UIAuditReport,
) -> dict[str, Any]:
    """Prepare proposed fixes for review without executing or applying them."""
    audit = parse_audit_report(report)

    if len(audit.issues) > MAX_PROPOSALS:
        raise ActionEngineError(
            f"Report contains more than {MAX_PROPOSALS} issues."
        )

    proposals = []

    for index, item in enumerate(audit.issues, start=1):
        fix = item.suggested_fix
        accepted, reason = validate_fix_code(fix.type, fix.code)

        proposals.append({
            "proposal_id": f"fix-{index:03d}",
            "element": item.element,
            "issue": item.issue,
            "severity": item.severity,
            "evidence": item.evidence,
            "confidence": item.confidence,
            "fix_type": fix.type,
            "code": fix.code,
            "rationale": fix.rationale,
            "validation": {
                "accepted_for_review": accepted,
                "reason": reason,
            },
            "status": "pending_review",
        })

    return {
        "summary": audit.summary,
        "total_issues": len(audit.issues),
        "accepted_for_review": sum(
            proposal["validation"]["accepted_for_review"]
            for proposal in proposals
        ),
        "rejected": sum(
            not proposal["validation"]["accepted_for_review"]
            for proposal in proposals
        ),
        "proposals": proposals,
    }
