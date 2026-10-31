"""Rule: credential fields filled directly instead of using n8n credentials.

Some nodes expose raw fields such as apiKey or accessToken. Filling them
stores the secret inside the workflow JSON, where exports and templates
spread it. n8n credentials keep the value encrypted and out of the file.
"""

from __future__ import annotations

from ..model import Finding, Workflow
from ._util import iter_items

RULE_ID = "credentials-outside-store"
SEVERITY = "high"
REMEDIATION = (
    "Create an n8n credential for this service and select it on the node; "
    "clear the raw credential field from the node parameters."
)

_CREDENTIAL_KEYS = {
    "apikey",
    "api_key",
    "apisecret",
    "clientsecret",
    "client_secret",
    "accesstoken",
    "access_token",
    "refreshtoken",
    "refresh_token",
    "password",
    "passwd",
    "privatekey",
    "private_key",
    "secretkey",
    "secret_key",
    "authtoken",
    "auth_token",
}


def detect(workflow: Workflow) -> list[Finding]:
    findings: list[Finding] = []
    for node in workflow.nodes:
        if node.short_type == "stickyNote":
            continue
        if node.credentials:
            continue
        for path, value in iter_items(node.parameters):
            key = path.rsplit(".", 1)[-1].split("[")[0].lower()
            if key not in _CREDENTIAL_KEYS:
                continue
            if not isinstance(value, str) or not value.strip():
                continue
            if value.lstrip().startswith("="):
                continue
            findings.append(
                Finding(
                    rule=RULE_ID,
                    severity=SEVERITY,
                    node=node.name,
                    message=(
                        f"Credential field '{path}' is filled directly on the node "
                        "instead of through n8n credentials."
                    ),
                    remediation=REMEDIATION,
                )
            )
    return findings
