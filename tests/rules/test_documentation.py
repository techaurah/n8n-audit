from pathlib import Path

from n8n_audit.loader import load_file
from n8n_audit.rules import documentation

FIXTURES = Path(__file__).resolve().parents[2] / "fixtures"


def test_fail_fixture_is_flagged():
    workflow = load_file(FIXTURES / "fail" / "documentation.json")[0]
    findings = documentation.detect(workflow)
    assert len(findings) == 1
    assert findings[0].severity == "low"


def test_pass_fixture_is_clean():
    workflow = load_file(FIXTURES / "pass" / "documentation.json")[0]
    assert documentation.detect(workflow) == []
