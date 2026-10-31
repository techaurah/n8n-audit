from pathlib import Path

from n8n_audit.loader import load_file, parse_workflow
from n8n_audit.rules import error_workflow

FIXTURES = Path(__file__).resolve().parents[2] / "fixtures"


def test_fail_fixture_is_flagged():
    workflow = load_file(FIXTURES / "fail" / "error-workflow.json")[0]
    findings = error_workflow.detect(workflow)
    assert len(findings) == 1
    assert findings[0].rule == "missing-error-workflow"


def test_pass_fixture_is_clean():
    workflow = load_file(FIXTURES / "pass" / "error-workflow.json")[0]
    assert error_workflow.detect(workflow) == []


def test_blank_error_workflow_is_flagged():
    workflow = parse_workflow({"name": "W", "nodes": [],
                                "settings": {"errorWorkflow": "  "}})
    assert len(error_workflow.detect(workflow)) == 1
