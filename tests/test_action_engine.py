
import json
import copy
import pytest

from action_engine import (
    ActionEngineError,
    extract_fix_proposals,
    parse_audit_report,
    prepare_review_package,
    validate_fix_code,
)

SAMPLE_REPORT = {
    "summary": "The login button has poor contrast.",
    "issues": [
        {
            "element": ".login-button",
            "issue": "Insufficient text contrast.",
            "severity": "medium",
            "evidence": "Button text is difficult to distinguish.",
            "suggested_fix": {
                "type": "css",
                "code": ".login-button { color: white; background: #222; }",
                "rationale": "Improve text contrast.",
            },
            "confidence": 0.95,
        }
    ],
}


def test_parse_valid_report():
    report = parse_audit_report(SAMPLE_REPORT)
    assert report.summary == SAMPLE_REPORT["summary"]
    assert len(report.issues) == 1


def test_parse_json_string():
    report = parse_audit_report(json.dumps(SAMPLE_REPORT))
    assert len(report.issues) == 1


def test_reject_invalid_json():
    with pytest.raises(ActionEngineError):
        parse_audit_report("{invalid json")


def test_reject_invalid_severity():
    invalid = copy.deepcopy(SAMPLE_REPORT)
    invalid["issues"][0]["severity"] = "extreme"
    with pytest.raises(ActionEngineError):
        parse_audit_report(invalid)


def test_extract_fix_proposals():
    proposals = extract_fix_proposals(SAMPLE_REPORT)
    assert len(proposals) == 1
    assert proposals[0]["fix_type"] == "css"
    assert proposals[0]["element"] == ".login-button"


def test_accept_basic_css():
    accepted, _ = validate_fix_code("css", ".button { color: white; }")
    assert accepted is True


def test_reject_css_import():
    accepted, _ = validate_fix_code(
        "css", "@import url('https://example.com/style.css');"
    )
    assert accepted is False


def test_reject_react_eval():
    accepted, _ = validate_fix_code("react", "eval(userInput)")
    assert accepted is False


def test_prepare_review_package():
    package = prepare_review_package(SAMPLE_REPORT)
    assert package["total_issues"] == 1
    assert package["accepted_for_review"] == 1
    assert package["proposals"][0]["status"] == "pending_review"


def test_unsafe_proposal_rejected_from_review():
    unsafe = copy.deepcopy(SAMPLE_REPORT)
    unsafe["issues"][0]["suggested_fix"]["code"] = (
        "@import url('https://example.com/style.css');"
    )
    package = prepare_review_package(unsafe)
    assert package["rejected"] == 1
    assert (
        package["proposals"][0]["validation"]["accepted_for_review"]
        is False
    )
