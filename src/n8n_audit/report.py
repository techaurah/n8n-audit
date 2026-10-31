"""Render an AuditReport as human-readable text or JSON."""

from __future__ import annotations

import json

from .model import AuditReport

_SEVERITY_LABEL = {"high": "HIGH", "medium": "MEDIUM", "low": "LOW", "info": "INFO"}


def format_json(report: AuditReport) -> str:
    return json.dumps(report.to_dict(), indent=2)


def format_text(report: AuditReport) -> str:
    lines: list[str] = []
    for result in report.results:
        lines.append(f"Workflow: {result.workflow} ({result.source})")
        if not result.findings:
            lines.append("  OK: no findings")
        for finding in result.findings:
            label = _SEVERITY_LABEL.get(finding.severity, finding.severity.upper())
            location = f" [node: {finding.node}]" if finding.node else ""
            lines.append(f"  [{label}] {finding.rule}{location}: {finding.message}")
            lines.append(f"         Fix: {finding.remediation}")
        lines.append("")
    counts = report.counts()
    lines.append(
        "Summary: {workflows} workflow(s), {total} finding(s) "
        "(high={high}, medium={medium}, low={low}, info={info})".format(
            workflows=len(report.results),
            total=len(report.findings),
            **counts,
        )
    )
    return "\n".join(lines)
