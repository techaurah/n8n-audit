from pathlib import Path

from n8n_audit.loader import load_file, parse_workflow
from n8n_audit.rules import secrets

FIXTURES = Path(__file__).resolve().parents[2] / "fixtures"


def test_fail_fixture_is_flagged():
    workflow = load_file(FIXTURES / "fail" / "secrets.json")[0]
    findings = secrets.detect(workflow)
    assert len(findings) >= 2
    assert all(f.severity == "high" for f in findings)


def test_pass_fixture_is_clean():
    workflow = load_file(FIXTURES / "pass" / "secrets.json")[0]
    assert secrets.detect(workflow) == []


def test_expression_referencing_env_is_allowed():
    workflow = parse_workflow({
        "name": "W",
        "nodes": [{"name": "Call", "type": "n8n-nodes-base.httpRequest",
                   "parameters": {"url": "={{ $env.API_BASE }}/x"}}],
    })
    assert secrets.detect(workflow) == []


def test_private_key_block_is_flagged():
    workflow = parse_workflow({
        "name": "W",
        "nodes": [{"name": "Note", "type": "n8n-nodes-base.code",
                   "parameters": {"jsCode": "-----BEGIN PRIVATE KEY-----"}}],
    })
    assert len(secrets.detect(workflow)) == 1
