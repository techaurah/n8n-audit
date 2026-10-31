from pathlib import Path

from n8n_audit.loader import load_file, parse_workflow
from n8n_audit.rules import retry

FIXTURES = Path(__file__).resolve().parents[2] / "fixtures"


def test_fail_fixture_is_flagged():
    workflow = load_file(FIXTURES / "fail" / "retry.json")[0]
    findings = retry.detect(workflow)
    assert len(findings) == 1
    assert findings[0].node == "Fetch Exchange Rates"


def test_pass_fixture_is_clean():
    workflow = load_file(FIXTURES / "pass" / "retry.json")[0]
    assert retry.detect(workflow) == []


def test_options_retry_block_counts():
    workflow = parse_workflow({
        "name": "W",
        "nodes": [{"name": "Call", "type": "n8n-nodes-base.httpRequest",
                   "parameters": {"url": "https://api.example.com",
                                  "options": {"retry": {"maxTries": 3}}}}],
    })
    assert retry.detect(workflow) == []


def test_on_error_setting_counts():
    workflow = parse_workflow({
        "name": "W",
        "nodes": [{"name": "Call", "type": "n8n-nodes-base.httpRequest",
                   "parameters": {"url": "https://api.example.com"},
                   "onError": "continueErrorOutput"}],
    })
    assert retry.detect(workflow) == []
