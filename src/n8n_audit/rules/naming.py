"""Rule: default node names in a production-sized workflow (report-only).

Nodes left with default names ('HTTP Request1', 'Code', 'IF') make a
workflow unreadable six months later and turn debugging into guesswork.
Report-only: this rule never fails a build on its own severity, it is low.
"""

from __future__ import annotations

import re

from ..model import Finding, Workflow

RULE_ID = "default-node-names"
SEVERITY = "low"
REMEDIATION = "Rename the node to say what it does in this workflow, e.g. 'Score lead and route'."

MIN_PRODUCTION_NODES = 8

_DEFAULT_NAMES = {
    "webhook",
    "http request",
    "code",
    "function",
    "functionitem",
    "if",
    "switch",
    "set",
    "edit fields (set)",
    "merge",
    "split in batches",
    "respond to webhook",
    "manual trigger",
    "schedule trigger",
    "form trigger",
    "item lists",
    "filter",
    "noop",
    "wait",
    "stop and error",
    "execute workflow",
    "google sheets",
    "gmail",
    "slack",
}

_TRAILING_NUMBER = re.compile(r"\s*\d+$")


def _is_default_name(name: str) -> bool:
    base = _TRAILING_NUMBER.sub("", name.strip().lower())
    return base in _DEFAULT_NAMES


def detect(workflow: Workflow) -> list[Finding]:
    if len(workflow.nodes) < MIN_PRODUCTION_NODES:
        return []
    findings: list[Finding] = []
    for node in workflow.nodes:
        if node.short_type == "stickyNote":
            continue
        if _is_default_name(node.name):
            findings.append(
                Finding(
                    rule=RULE_ID,
                    severity=SEVERITY,
                    node=node.name,
                    message=f"Node still has its default name ('{node.name}').",
                    remediation=REMEDIATION,
                )
            )
    return findings
