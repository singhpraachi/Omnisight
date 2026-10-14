\# OmniSight Action Engine



\## Overview



The Action Engine processes UI audit reports from a Vision-Language Model (VLM) and prepares suggested fixes for human review.



It supports CSS and React fix proposals. It validates report structure, extracts proposed fixes, performs basic code checks, and creates a review package.



The Action Engine does not execute proposed code or automatically modify the application.



\## Features



\- Parse audit reports from JSON strings, dictionaries, or validated report objects.

\- Validate reports using Pydantic models.

\- Extract proposed fixes with element, issue, severity, evidence, confidence, code, and rationale.

\- Perform basic pattern checks on CSS and React proposals.

\- Prepare review packages with validation results and pending-review statuses.

\- Reject reports containing more than 100 issues.



\## Expected report structure



Each issue contains:



\- `element`: affected UI element.

\- `issue`: description of the visual problem.

\- `severity`: `low`, `medium`, `high`, or `critical`.

\- `evidence`: evidence supporting the finding.

\- `suggested\_fix`: fix type, code, and rationale.

\- `confidence`: value between 0 and 1.



\## Usage



```python

from action\_engine import prepare\_review\_package



report = {

&#x20;   "summary": "The login button has poor contrast.",

&#x20;   "issues": \[

&#x20;       {

&#x20;           "element": ".login-button",

&#x20;           "issue": "Insufficient text contrast.",

&#x20;           "severity": "medium",

&#x20;           "evidence": "The button text is difficult to distinguish.",

&#x20;           "suggested\_fix": {

&#x20;               "type": "css",

&#x20;               "code": ".login-button { color: white; background: #222; }",

&#x20;               "rationale": "Improve text contrast."

&#x20;           },

&#x20;           "confidence": 0.95

&#x20;       }

&#x20;   ]

}



review\_package = prepare\_review\_package(report)

print(review\_package)

```



\## Run tests



From the repository root, with the project virtual environment activated:



```powershell

python -m pytest tests\\test\_action\_engine.py -v

```



\## Safety limitations



Code checks use a limited set of pattern-based rules. They are not a complete security analysis and may miss unsafe code or reject legitimate code.



A proposal marked as accepted is only accepted for review. It is not guaranteed to be safe. Human review is required before any proposed change is applied.



\## Current scope



The Action Engine parses reports and prepares fix proposals. It does not yet apply fixes, edit source files, create Git commits, or open pull requests automatically.

