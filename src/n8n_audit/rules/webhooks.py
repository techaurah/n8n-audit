"""Rule: webhook trigger without authentication.

An unauthenticated webhook is a public endpoint anyone can post to. Where
the export exposes the authentication setting, it must not be empty or
'none' on a production workflow.
"""

from __future__ import annotations

from ..model import Finding, Workflow

RULE_ID = "webhook-without-auth"
SEVERITY = "high"
REMEDIATION = (
    "Enable header auth, basic auth or JWT auth on the webhook node and "
    "share the credential only with the calling system."
)

_SAFE_AUTH = {"headerauth", "basicauth", "jwtauth", "oauthtoken"}


def detect(workflow: Workflow) -> list[Finding]:
    findings: list[Finding] = []
    for node in workflow.nodes:
        if node.short_type != "webhook":
            continue
        auth = node.parameters.get("authentication")
        if isinstance(auth, str) and auth.strip().lower() in _SAFE_AUTH:
            continue
        if node.credentials:
            continue
        findings.append(
            Finding(
                rule=RULE_ID,
                severity=SEVERITY,
                node=node.name,
                message="Webhook trigger has no authentication configured.",
                remediation=REMEDIATION,
            )
        )
    return findings
