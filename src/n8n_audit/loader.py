"""Load exported n8n workflow JSON files into the model."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .model import Node, Workflow


class LoaderError(Exception):
    """Raised when a file cannot be parsed as an n8n workflow export."""


def parse_workflow(data: Any, source: str = "<memory>") -> Workflow:
    """Build a Workflow from already-decoded JSON data."""
    if not isinstance(data, dict):
        raise LoaderError(f"{source}: expected a workflow object, got {type(data).__name__}")
    raw_nodes = data.get("nodes")
    if not isinstance(raw_nodes, list):
        raise LoaderError(f"{source}: missing or invalid 'nodes' list, is this an n8n export?")
    nodes: list[Node] = []
    for index, raw_node in enumerate(raw_nodes):
        if not isinstance(raw_node, dict):
            raise LoaderError(f"{source}: node at index {index} is not an object")
        nodes.append(
            Node(
                id=str(raw_node.get("id", f"node-{index}")),
                name=str(raw_node.get("name", f"node-{index}")),
                type=str(raw_node.get("type", "")),
                parameters=raw_node.get("parameters") or {},
                credentials=raw_node.get("credentials") or {},
                raw=raw_node,
            )
        )
    settings = data.get("settings") or {}
    if not isinstance(settings, dict):
        settings = {}
    return Workflow(
        name=str(data.get("name") or "Untitled workflow"),
        nodes=nodes,
        settings=settings,
        source=source,
        raw=data,
    )


def load_file(path: str | Path) -> list[Workflow]:
    """Load one JSON file. A file may hold one workflow object or a list."""
    file_path = Path(path)
    try:
        text = file_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise LoaderError(f"cannot read {file_path}: {exc}") from exc
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise LoaderError(f"{file_path}: invalid JSON ({exc})") from exc
    if isinstance(data, list):
        return [parse_workflow(item, source=str(file_path)) for item in data]
    return [parse_workflow(data, source=str(file_path))]


def collect_paths(paths: list[str]) -> list[Path]:
    """Expand CLI path arguments: files stay, directories yield *.json."""
    collected: list[Path] = []
    for raw in paths:
        candidate = Path(raw)
        if candidate.is_dir():
            collected.extend(sorted(candidate.glob("*.json")))
        else:
            collected.append(candidate)
    return collected
