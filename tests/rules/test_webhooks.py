from pathlib import Path

from n8n_audit.loader import load_file, parse_workflow
from n8n_audit.rules import webhooks

FIXTURES = Path(__file__).resolve().parents[2] / "fixtures"


def test_fail_fixture_is_flagged():
    workflow = load_file(FIXTURES / "fail" / "webhooks.json")[0]
    findings = webhooks.detect(workflow)
    assert len(findings) == 1
    assert findings[0].severity == "high"


def test_pass_fixture_is_clean():
    workflow = load_file(FIXTURES / "pass" / "webhooks.json")[0]
    assert webhooks.detect(workflow) == []


def test_missing_authentication_key_is_flagged():
    workflow = parse_workflow({
        "name": "W",
        "nodes": [{"name": "Hook", "type": "n8n-nodes-base.webhook",
                   "parameters": {"path": "x"}}],
    })
    assert len(webhooks.detect(workflow)) == 1


def test_non_webhook_nodes_ignored():
    workflow = parse_workflow({
        "name": "W",
        "nodes": [{"name": "Start", "type": "n8n-nodes-base.manualTrigger",
                   "parameters": {}}],
    })
    assert webhooks.detect(workflow) == []
