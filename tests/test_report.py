import json
from pathlib import Path

from n8n_audit.cli import audit_workflows, main
from n8n_audit.loader import load_file
from n8n_audit.model import AuditReport, Finding, WorkflowResult
from n8n_audit.report import format_json, format_text
from n8n_audit.rules import ALL_RULES

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures"


def _report(*findings):
    return AuditReport(
        results=[WorkflowResult(workflow="W", source="w.json", findings=list(findings))]
    )


def _finding(severity):
    return Finding(rule="r", severity=severity, message="m", remediation="fix it")


def test_text_report_empty_is_ok():
    text = format_text(_report())
    assert "OK: no findings" in text
    assert "0 finding(s)" in text


def test_text_report_lists_findings_and_fix():
    text = format_text(_report(_finding("high")))
    assert "[HIGH] r" in text
    assert "Fix: fix it" in text


def test_json_report_round_trips():
    data = json.loads(format_json(_report(_finding("medium"))))
    assert data["summary"]["findings"] == 1
    assert data["summary"]["by_severity"]["medium"] == 1
    assert data["results"][0]["findings"][0]["rule"] == "r"


def test_exit_code_thresholds():
    assert _report().exit_code() == 0
    assert _report(_finding("medium")).exit_code() == 0
    assert _report(_finding("medium")).exit_code(fail_on="medium") == 1
    assert _report(_finding("high")).exit_code() == 1
    assert _report(_finding("low")).exit_code(fail_on="low") == 1


def test_golden_fixture_has_zero_findings():
    workflow = load_file(FIXTURES / "golden" / "lead-automation-hardened.json")[0]
    findings = []
    for detector in ALL_RULES:
        findings.extend(detector(workflow))
    assert findings == []


def test_cli_exit_codes_end_to_end(capsys):
    golden = str(FIXTURES / "golden" / "lead-automation-hardened.json")
    failing = str(FIXTURES / "fail" / "secrets.json")
    assert main([golden]) == 0
    capsys.readouterr()
    assert main([failing]) == 1
    out = capsys.readouterr().out
    assert "secrets-in-parameters" in out
    assert main(["--format", "json", failing]) == 1
    data = json.loads(capsys.readouterr().out)
    assert data["summary"]["findings"] >= 1
    assert main([str(FIXTURES / "does-not-exist.json")]) == 2


def test_audit_workflows_aggregates():
    report = audit_workflows([str(FIXTURES / "fail")])
    assert len(report.results) >= 8
    assert report.exit_code() == 1
