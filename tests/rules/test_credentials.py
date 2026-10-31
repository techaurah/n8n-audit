from pathlib import Path

from n8n_audit.loader import load_file, parse_workflow
from n8n_audit.rules import credentials

FIXTURES = Path(__file__).resolve().parents[2] / "fixtures"


def test_fail_fixture_is_flagged():
    workflow = load_file(FIXTURES / "fail" / "credentials.json")[0]
    findings = credentials.detect(workflow)
    assert len(findings) == 1
    assert findings[0].node == "Send SMS via Gateway"


def test_pass_fixture_is_clean():
    workflow = load_file(FIXTURES / "pass" / "credentials.json")[0]
    assert credentials.detect(workflow) == []


def test_node_with_credentials_store_is_clean():
    workflow = parse_workflow({
        "name": "W",
        "nodes": [{"name": "Send", "type": "n8n-nodes-base.twilio",
                   "parameters": {"apiKey": "leftover-ui-value"},
                   "credentials": {"twilioApi": {"id": "1", "name": "Twilio"}}}],
    })
    assert credentials.detect(workflow) == []


def test_empty_and_expression_values_are_clean():
    workflow = parse_workflow({
        "name": "W",
        "nodes": [{"name": "Send", "type": "x.y",
                   "parameters": {"password": "", "accessToken": "={{ $env.T }}"}}],
    })
    assert credentials.detect(workflow) == []
