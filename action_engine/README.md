# Action Engine

## Overview

The Action Engine parses UI audit reports, validates suggested fixes, and prepares proposals for review before integration with OmniSight.

It accepts structured audit reports and produces validated fix proposals without executing or automatically applying suggested code.

## Features

- Parse reports supplied as JSON strings, dictionaries, or validated report models.
- Validate report fields and suggested-fix types using Pydantic models.
- Extract individual fix proposals from an audit report.
- Perform basic safety checks on CSS and React fix code.
- Prepare a review package with proposal validation results and summary counts.
- Support human review before fixes are applied.

## Usage

```python
from action_engine import (
    parse_audit_report,
    extract_fix_proposals,
    prepare_review_package,
)

report = {
    "summary": "One UI issue detected",
    "issues": [
        {
            "element": "Submit button",
            "issue": "Insufficient color contrast",
            "severity": "medium",
            "evidence": "The button text is difficult to read.",
            "suggested_fix": {
                "type": "css",
                "code": "color: #222; background-color: #fff;",
                "rationale": "Improve text readability.",
            },
            "confidence": 0.95,
        }
    ],
}

validated_report = parse_audit_report(report)
proposals = extract_fix_proposals(validated_report)
review_package = prepare_review_package(validated_report)

print(proposals)
print(review_package)
```

## Run tests

From the repository root:

```powershell
python -m pytest tests\test_action_engine.py -v
```

## Integration workflow

1. Receive a UI audit report from the VLM analyzer.
2. Parse and validate the report.
3. Extract suggested fix proposals.
4. Run basic safety checks.
5. Present the proposals and validation results for human review.
6. Leave applying fixes and creating pull requests to a separate, approved integration workflow.

## Safety and scope

The Action Engine does not execute proposed code or automatically modify application files. Its checks are basic pattern-based safeguards and are not a complete security analysis. Proposals must be reviewed before application.

## Current scope

This component provides report parsing, proposal extraction, basic validation, and review-package preparation. Full browser integration, automatic fix application, and pull-request creation are outside its current scope.