"""Core data model: parsed workflows, findings and audit results."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

SEVERITY_ORDER = {"info": 0, "low": 1, "medium": 2, "high": 3}


@dataclass
class Node:
    """A single n8n node inside a workflow."""

    id: str
    name: str
    type: str
    parameters: dict[str, Any] = field(default_factory=dict)
    credentials: dict[str, Any] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)

    @property
    def short_type(self) -> str:
        """The node type without the package prefix, e.g. 'webhook'."""
        return self.type.rsplit(".", 1)[-1] if "." in self.type else self.type


@dataclass
class Workflow:
    """A parsed n8n workflow export."""

    name: str
    nodes: list[Node] = field(default_factory=list)
    settings: dict[str, Any] = field(default_factory=dict)
    source: str = "<memory>"
    raw: dict[str, Any] = field(default_factory=dict)

    def nodes_of_type(self, *fragments: str) -> list[Node]:
        """Return nodes whose type contains any of the given fragments."""
        lowered = tuple(f.lower() for f in fragments)
        return [n for n in self.nodes if any(f in n.type.lower() for f in lowered)]


@dataclass
class Finding:
    """One rule hit on one workflow (optionally tied to one node)."""

    rule: str
    severity: str
    message: str
    remediation: str
    node: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule": self.rule,
            "severity": self.severity,
            "node": self.node,
            "message": self.message,
            "remediation": self.remediation,
        }


@dataclass
class WorkflowResult:
    """All findings for one workflow."""

    workflow: str
    source: str
    findings: list[Finding] = field(default_factory=list)

    def counts(self) -> dict[str, int]:
        counts = {level: 0 for level in SEVERITY_ORDER}
        for finding in self.findings:
            counts[finding.severity] = counts.get(finding.severity, 0) + 1
        return counts

    def max_severity(self) -> str | None:
        if not self.findings:
            return None
        return max(self.findings, key=lambda f: SEVERITY_ORDER[f.severity]).severity


@dataclass
class AuditReport:
    """Findings across every audited workflow."""

    results: list[WorkflowResult] = field(default_factory=list)

    @property
    def findings(self) -> list[Finding]:
        return [f for result in self.results for f in result.findings]

    def counts(self) -> dict[str, int]:
        counts = {level: 0 for level in SEVERITY_ORDER}
        for finding in self.findings:
            counts[finding.severity] = counts.get(finding.severity, 0) + 1
        return counts

    def exit_code(self, fail_on: str = "high") -> int:
        """1 when any finding is at or above the fail_on severity, else 0."""
        threshold = SEVERITY_ORDER[fail_on]
        for finding in self.findings:
            if SEVERITY_ORDER[finding.severity] >= threshold:
                return 1
        return 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "summary": {
                "workflows": len(self.results),
                "findings": len(self.findings),
                "by_severity": self.counts(),
            },
            "results": [
                {
                    "workflow": result.workflow,
                    "source": result.source,
                    "findings": [f.to_dict() for f in result.findings],
                }
                for result in self.results
            ],
        }
