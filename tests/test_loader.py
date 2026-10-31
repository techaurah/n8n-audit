from pathlib import Path

import pytest

from n8n_audit.loader import LoaderError, load_file, parse_workflow

ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "fixtures" / "golden" / "lead-automation-hardened.json"


def test_load_golden_fixture():
    workflows = load_file(GOLDEN)
    assert len(workflows) == 1
    workflow = workflows[0]
    assert workflow.name == "Lead Automation (Hardened)"
    assert len(workflow.nodes) == 9
    assert workflow.settings.get("errorWorkflow")


def test_load_list_of_workflows(tmp_path):
    file_path = tmp_path / "multi.json"
    file_path.write_text('[{"name": "A", "nodes": []}, {"name": "B", "nodes": []}]')
    workflows = load_file(file_path)
    assert [w.name for w in workflows] == ["A", "B"]


def test_load_missing_file(tmp_path):
    with pytest.raises(LoaderError):
        load_file(tmp_path / "nope.json")


def test_load_invalid_json(tmp_path):
    file_path = tmp_path / "broken.json"
    file_path.write_text("{not json")
    with pytest.raises(LoaderError):
        load_file(file_path)


def test_parse_rejects_non_workflow():
    with pytest.raises(LoaderError):
        parse_workflow({"name": "no nodes here"})
    with pytest.raises(LoaderError):
        parse_workflow(["not", "a", "dict"])


def test_node_defaults():
    workflow = parse_workflow({"name": "W", "nodes": [{"name": "Only Name"}]})
    node = workflow.nodes[0]
    assert node.parameters == {}
    assert node.credentials == {}
