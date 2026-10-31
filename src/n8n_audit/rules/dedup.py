"""Rule: no deduplication pattern near a webhook or form trigger.

Webhook and form triggers fire at least once, not exactly once: senders
retry, users double-submit, providers redeliver. Without a deduplication
step, the same lead gets emailed twice and written to the CRM twice.

The detector is a documented heuristic: a workflow passes when any node
name or parameter text mentions deduplication, idempotency or processed
record checks, or when a node type known for lookup-before-write is
present next to the trigger.
"""

from __future__ import annotations

from ..model import Finding, Workflow
from ._util import iter_strings

RULE_ID = "missing-deduplication"
SEVERITY = "medium"
REMEDIATION = (
    "Add a deduplication step after the trigger: check a unique key (lead "
    "id, email, submission id) against stored processed ids and stop early "
    "when it was already handled."
)

_TRIGGER_TYPES = ("webhook", "formtrigger")
_KEYWORDS = (
    "dedup",
    "duplicate",
    "idempoten",
    "already processed",
    "processed ids",
    "processedids",
    "unique check",
    "seen ids",
)


def _has_dedup_pattern(workflow: Workflow) -> bool:
    for node in workflow.nodes:
        if any(keyword in node.name.lower() for keyword in _KEYWORDS):
            return True
        for _path, text in iter_strings(node.parameters):
            lowered = text.lower()
            if any(keyword in lowered for keyword in _KEYWORDS):
                return True
    return False


def detect(workflow: Workflow) -> list[Finding]:
    triggers = [
        node
        for node in workflow.nodes
        if node.short_type.lower() in _TRIGGER_TYPES
    ]
    if not triggers:
        return []
    if _has_dedup_pattern(workflow):
        return []
    return [
        Finding(
            rule=RULE_ID,
            severity=SEVERITY,
            node=triggers[0].name,
            message=(
                "Workflow accepts webhook or form submissions but shows no "
                "deduplication pattern; redeliveries will be processed twice."
            ),
            remediation=REMEDIATION,
        )
    ]
