from pathlib import Path

from n8n_audit.loader import load_file, parse_workflow
from n8n_audit.rules import naming

FIXTURES = Path(__file__).resolve().parents[2] / "fixtures"


def test_fail_fixture_is_flagged():
    workflow = load_file(FIXTURES / "fail" / "naming.json")[0]
    findings = naming.detect(workflow)
    flagged = {f.node for f in findings}
    assert {"Webhook", "HTTP Request", "Code", "Code1", "IF", "Set", "Merge"} <= flagged
    assert all(f.severity == "low" for f in findings)


def test_pass_fixture_is_clean():
    workflow = load_file(FIXTURES / "pass" / "naming.json")[0]
    assert naming.detect(workflow) == []


def test_small_workflows_are_not_flagged():
    workflow = parse_workflow({
        "name": "W",
        "nodes": [{"name": "Code", "type": "n8n-nodes-base.code", "parameters": {}},
                  {"name": "IF", "type": "n8n-nodes-base.if", "parameters": {}}],
    })
    assert naming.detect(workflow) == []
