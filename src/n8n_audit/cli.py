"""Command line interface for n8n-audit."""

from __future__ import annotations

import argparse
import sys

from . import __version__
from .loader import LoaderError, collect_paths, load_file
from .model import AuditReport, WorkflowResult
from .report import format_json, format_text
from .rules import ALL_RULES


def audit_workflows(paths: list[str]) -> AuditReport:
    report = AuditReport()
    for file_path in collect_paths(paths):
        for workflow in load_file(file_path):
            findings = []
            for detector in ALL_RULES:
                findings.extend(detector(workflow))
            findings.sort(key=lambda f: f.rule)
            report.results.append(
                WorkflowResult(
                    workflow=workflow.name,
                    source=workflow.source,
                    findings=findings,
                )
            )
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="n8n-audit",
        description=(
            "Statically audit exported n8n workflow JSON for production "
            "readiness problems: secrets, unauthenticated webhooks, missing "
            "error workflows, missing deduplication, missing retries and more."
        ),
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="Workflow JSON files or directories containing them.",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Report format (default: text).",
    )
    parser.add_argument(
        "--fail-on",
        choices=["high", "medium", "low", "info"],
        default="high",
        help="Lowest severity that makes the exit code 1 (default: high).",
    )
    parser.add_argument("--version", action="version", version=f"n8n-audit {__version__}")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        report = audit_workflows(args.paths)
    except LoaderError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if not report.results:
        print("error: no workflow files found in the given paths", file=sys.stderr)
        return 2
    output = format_json(report) if args.format == "json" else format_text(report)
    print(output)
    return report.exit_code(fail_on=args.fail_on)


if __name__ == "__main__":
    raise SystemExit(main())
