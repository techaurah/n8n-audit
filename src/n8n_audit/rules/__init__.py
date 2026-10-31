"""Rule registry: every detector is a function Workflow -> list[Finding]."""

from __future__ import annotations

from collections.abc import Callable

from ..model import Finding, Workflow
from . import (
    credentials,
    dedup,
    documentation,
    error_workflow,
    naming,
    retry,
    secrets,
    webhooks,
)

Detector = Callable[[Workflow], list[Finding]]

ALL_RULES: list[Detector] = [
    secrets.detect,
    credentials.detect,
    webhooks.detect,
    error_workflow.detect,
    dedup.detect,
    retry.detect,
    naming.detect,
    documentation.detect,
]

__all__ = ["ALL_RULES", "Detector"]
