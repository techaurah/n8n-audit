"""Shared helpers for rule detectors."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any


def iter_strings(value: Any, path: str = "") -> Iterator[tuple[str, str]]:
    """Yield (path, string) for every string inside a nested structure."""
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from iter_strings(item, f"{path}.{key}" if path else str(key))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from iter_strings(item, f"{path}[{index}]")


def iter_items(value: Any, path: str = "") -> Iterator[tuple[str, Any]]:
    """Yield (path, value) for every leaf value inside a nested structure."""
    if isinstance(value, dict):
        for key, item in value.items():
            yield from iter_items(item, f"{path}.{key}" if path else str(key))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from iter_items(item, f"{path}[{index}]")
    else:
        yield path, value
