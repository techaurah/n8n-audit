"""Rule: no sticky-note documentation in the workflow (report-only).

Sticky notes are the only documentation that travels with an exported
n8n workflow. A workflow with none explains itself to nobody: not to the
next maintainer, not to the client, not to future you.
"""

from __future__ import annotations

from ..model import Finding, Workflow

RULE_ID = "missing-documentation"
SEVERITY = "low"
REMEDIATION = (
    "Add at least one sticky note to the canvas explaining what the "
    "workflow does, what triggers it and who owns it."
)


def detect(workflow: Workflow) -> list[Finding]:
    if any(node.short_type == "stickyNote" for node in workflow.nodes):
        return []
    return [
        Finding(
            rule=RULE_ID,
            severity=SEVERITY,
            message="Workflow contains no sticky-note documentation.",
            remediation=REMEDIATION,
        )
    ]
