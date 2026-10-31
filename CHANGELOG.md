# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-10-31

### Added

- CLI (`n8n-audit`) that statically analyses exported n8n workflow JSON
  from files or directories, with human-readable and JSON reports.
- Eight deterministic rules: `secrets-in-parameters`,
  `credentials-outside-store`, `webhook-without-auth`,
  `missing-error-workflow`, `missing-deduplication`, `http-without-retry`,
  `default-node-names` (report-only) and `missing-documentation`
  (report-only).
- Severity per finding, a one-line remediation per rule, and CI-friendly
  exit codes (exit 1 on high severity by default, exit 2 on unreadable
  input).
- Seventeen fixture workflows: a hardened lead-automation "golden"
  workflow that passes every rule, plus a pass and a fail fixture per rule.
- Full pytest suite covering the loader, the reporters, every rule and
  end-to-end CLI exit codes.
- Rule reference in `docs/rules.md` and a real generated report in
  `docs/example-report.md`.
