"""Rule: no error workflow configured.

Without an error workflow, a failed production execution is silent: the
lead, order or ticket the workflow existed to handle simply never lands,
and nobody is told.
"""

from __future__ import annotations

from ..model import Finding, Workflow

RULE_ID = "missing-error-workflow"
SEVERITY = "high"
REMEDIATION = (
    "Set an error workflow in the workflow settings (Settings > Error "
    "Workflow) that alerts a human and logs the failed execution."
)


def detect(workflow: Workflow) -> list[Finding]:
    error_workflow = workflow.settings.get("errorWorkflow")
    if isinstance(error_workflow, str) and error_workflow.strip():
        return []
    return [
        Finding(
            rule=RULE_ID,
            severity=SEVERITY,
            message="Workflow has no error workflow configured in its settings.",
            remediation=REMEDIATION,
        )
    ]
