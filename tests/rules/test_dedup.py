from pathlib import Path

from n8n_audit.loader import load_file, parse_workflow
from n8n_audit.rules import dedup

FIXTURES = Path(__file__).resolve().parents[2] / "fixtures"


def test_fail_fixture_is_flagged():
    workflow = load_file(FIXTURES / "fail" / "dedup.json")[0]
    findings = dedup.detect(workflow)
    assert len(findings) == 1
    assert findings[0].severity == "medium"


def test_pass_fixture_is_clean():
    workflow = load_file(FIXTURES / "pass" / "dedup.json")[0]
    assert dedup.detect(workflow) == []


def test_no_trigger_no_finding():
    workflow = parse_workflow({
        "name": "W",
        "nodes": [{"name": "Start", "type": "n8n-nodes-base.manualTrigger",
                   "parameters": {}}],
    })
    assert dedup.detect(workflow) == []


def test_form_trigger_also_requires_dedup():
    workflow = parse_workflow({
        "name": "W",
        "nodes": [{"name": "Form", "type": "n8n-nodes-base.formTrigger",
                   "parameters": {}}],
    })
    assert len(dedup.detect(workflow)) == 1
