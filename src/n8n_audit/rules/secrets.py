"""Rule: pasted secret patterns inside node parameters.

Hardcoded keys in node parameters end up in exported JSON, git history,
screenshots and shared templates. They belong in n8n credentials or
environment variables, never in the workflow file itself.
"""

from __future__ import annotations

import re

from ..model import Finding, Workflow
from ._util import iter_strings

RULE_ID = "secrets-in-parameters"
SEVERITY = "high"
REMEDIATION = (
    "Move the secret into an n8n credential or an environment variable and "
    "reference it; rotate the exposed value, it has left the building."
)

_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("OpenAI-style API key", re.compile(r"sk-(?:proj-)?[A-Za-z0-9_\-]{16,}")),
    ("GitHub token", re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}")),
    ("Slack token", re.compile(r"xox[baprs]-[A-Za-z0-9\-]{10,}")),
    ("AWS access key id", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("private key block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("JSON web token", re.compile(r"eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}")),
    (
        "credential assignment in text",
        re.compile(
            r"(?i)(api[_-]?key|client[_-]?secret|access[_-]?token|password|passwd)"
            r"\s*[:=]\s*[\"']?[A-Za-z0-9_\-/+]{8,}"
        ),
    ),
    (
        "password embedded in URL",
        re.compile(r"[a-zA-Z][a-zA-Z0-9+.\-]*://[^\s/:@]+:[^\s/@]{4,}@"),
    ),
]


def _is_expression(value: str) -> bool:
    return value.lstrip().startswith("=")


def detect(workflow: Workflow) -> list[Finding]:
    findings: list[Finding] = []
    for node in workflow.nodes:
        if node.short_type == "stickyNote":
            continue
        for path, text in iter_strings(node.parameters):
            if _is_expression(text):
                continue
            for label, pattern in _PATTERNS:
                if pattern.search(text):
                    findings.append(
                        Finding(
                            rule=RULE_ID,
                            severity=SEVERITY,
                            node=node.name,
                            message=f"Possible {label} pasted into parameter '{path}'.",
                            remediation=REMEDIATION,
                        )
                    )
                    break
    return findings
