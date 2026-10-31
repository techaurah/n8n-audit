"""Rule: HTTP nodes calling external APIs without retry or error handling.

External APIs rate-limit (HTTP 429) and fail transiently. An HTTP node with
no retry setting and no error handling turns a one-second blip into lost
work, exactly the failure class behind most silent automation breakage.
"""

from __future__ import annotations

from ..model import Finding, Node, Workflow

RULE_ID = "http-without-retry"
SEVERITY = "medium"
REMEDIATION = (
    "Enable 'Retry On Fail' on the HTTP node (3 or more tries with a wait "
    "between tries) or set explicit error handling for the node."
)


def _has_retry_handling(node: Node) -> bool:
    if node.raw.get("retryOnFail") is True:
        return True
    if node.raw.get("onError"):
        return True
    options = node.parameters.get("options")
    if isinstance(options, dict):
        if options.get("retry"):
            return True
        if options.get("retryOnFail"):
            return True
    return False


def detect(workflow: Workflow) -> list[Finding]:
    findings: list[Finding] = []
    for node in workflow.nodes:
        if node.short_type != "httpRequest":
            continue
        if _has_retry_handling(node):
            continue
        findings.append(
            Finding(
                rule=RULE_ID,
                severity=SEVERITY,
                node=node.name,
                message=(
                    "HTTP request node has no retry on fail and no explicit "
                    "error handling; a transient API error will drop this work."
                ),
                remediation=REMEDIATION,
            )
        )
    return findings
