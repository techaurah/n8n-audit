<h1 align="center">n8n-audit</h1>

<p align="center"><strong>n8n-audit is a production-readiness linter for n8n workflows that checks exported workflow JSON for the failure classes that break automations in production, in seconds, locally or in CI.</strong></p>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-blue" alt="License: MIT"/>
  <img src="https://img.shields.io/badge/python-%3E%3D3.10-blue" alt="Python 3.10 or newer"/>
  <img src="https://img.shields.io/badge/version-0.1.0-green" alt="Version 0.1.0"/>
  <img src="https://img.shields.io/badge/dependencies-none-brightgreen" alt="No runtime dependencies"/>
</p>

<p align="center">
  <a href="docs/rules.md">Rule reference</a> ·
  <a href="docs/example-report.md">Example report</a> ·
  <a href="#examples">Examples (fixtures)</a> ·
  <a href="https://github.com/techaurah/n8n-audit/issues">Roadmap (issues)</a> ·
  <a href="https://github.com/techaurah/n8n-audit/discussions">Discussions</a> ·
  <a href="https://techaurah.com">TechAurah</a>
</p>

## The problem

n8n workflows get promoted from tutorial state to production carrying
known, nameable problems: no error workflow, so failures are silent.
Secrets pasted into nodes, so exports leak keys. Webhooks with no
authentication. No deduplication, so a redelivered webhook emails a
lead twice. HTTP nodes with no retry, so one rate-limit response loses
the work forever.

Workflow owners (freelancers, agencies, self-hosting small businesses)
usually discover these when a client workflow silently drops leads.
n8n itself is one of the largest open-source projects in the world
(209,203 stars on GitHub, read 2026-10-31, with 13,809 public
repositories under the `n8n` topic), yet nothing established audits an
exported workflow file for these classes before it ships.

This project does that check. It does not run, schedule or modify
workflows, and it never calls the network: it reads exported JSON and
reports.

## Demo

Auditing the hardened example workflow that ships in this repo:

```console
$ n8n-audit fixtures/golden/lead-automation-hardened.json
Workflow: Lead Automation (Hardened) (fixtures/golden/lead-automation-hardened.json)
  OK: no findings

Summary: 1 workflow(s), 0 finding(s) (high=0, medium=0, low=0, info=0)
```

Auditing a workflow with problems (exit code 1, ready for CI):

```console
$ n8n-audit fixtures/fail/
...
Summary: 8 workflow(s), 24 finding(s) (high=6, medium=4, low=14, info=0)
```

A full real report, in text and JSON form, is in
[docs/example-report.md](docs/example-report.md).

## Quickstart

Prerequisites: Python 3.10 or newer. No accounts, no API keys, no
services.

```bash
pip install n8n-audit
```

(From source: `pip install -e .` inside a clone of this repository.)

Export any workflow from n8n (workflow menu, Download) and audit it:

```bash
n8n-audit my-workflow.json
```

Audit every export in a directory, as JSON, failing CI on any medium
or worse finding:

```bash
n8n-audit exports/ --format json --fail-on medium
```

Expected result: a report like the demo above, and an exit code of 0
when nothing at or above the fail threshold is found.

## What it does

- [x] **`secrets-in-parameters`** (high): keys, tokens, private keys and credential assignments pasted into node parameters. [Rule](docs/rules.md#1-secrets-in-parameters-high)
- [x] **`credentials-outside-store`** (high): credential fields filled directly on a node instead of through n8n credentials. [Rule](docs/rules.md#2-credentials-outside-store-high)
- [x] **`webhook-without-auth`** (high): webhook triggers with no authentication where the export exposes the setting. [Rule](docs/rules.md#3-webhook-without-auth-high)
- [x] **`missing-error-workflow`** (high): no error workflow configured, so failures are silent. [Rule](docs/rules.md#4-missing-error-workflow-high)
- [x] **`missing-deduplication`** (medium): webhook or form trigger with no deduplication pattern. [Rule](docs/rules.md#5-missing-deduplication-medium)
- [x] **`http-without-retry`** (medium): HTTP nodes calling external APIs with no retry and no error handling. [Rule](docs/rules.md#6-http-without-retry-medium)
- [x] **`default-node-names`** (low, report-only): default node names left in production-sized workflows. [Rule](docs/rules.md#7-default-node-names-low-report-only)
- [x] **`missing-documentation`** (low, report-only): no sticky-note documentation on the canvas. [Rule](docs/rules.md#8-missing-documentation-low-report-only)

Every finding includes the workflow, the node when relevant, and a
one-line remediation.

## Configuration

n8n-audit has no config file and reads no environment variables. All
behaviour is set by command line flags:

| Flag | Values | Default | Purpose |
|---|---|---|---|
| `--format` | `text`, `json` | `text` | Report format |
| `--fail-on` | `high`, `medium`, `low`, `info` | `high` | Lowest severity that produces exit code 1 |
| `--version` | | | Print the version |

Exit codes: `0` means no findings at or above the threshold, `1` means
findings at or above it, `2` means the input could not be read or
parsed. Inputs may be single files, several files, directories (all
`*.json` inside are audited), or a mix. A file holding a JSON list of
workflows is supported, matching multi-workflow exports.

## Examples

Everything below runs offline on included fixture data. No credentials
are needed for any of them.

| Example | What it shows | Time |
|---|---|---|
| `fixtures/golden/lead-automation-hardened.json` | A production lead-automation workflow that passes all 8 rules: authenticated webhook, deduplication, error workflow, retries, credentials store, sticky-note docs | 10 seconds |
| `fixtures/pass/*.json` | One minimal passing workflow per rule | 10 seconds each |
| `fixtures/fail/*.json` | One failing workflow per rule: run `n8n-audit fixtures/fail/` and read the report against [the rule reference](docs/rules.md) | 1 minute |

## Roadmap

- **Now:** v0.1, the 8 rules above, text and JSON reports, CI exit codes.
- **Next:** more node-type coverage (queues, databases, AI agent nodes),
  SARIF output for GitHub code scanning, per-rule ignore comments.
- **Later:** an n8n community node or editor integration, if the CLI
  proves the rules are useful. Roadmap items are tracked as issues.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md), find a
`good first issue`, and open a pull request that links the issue and
passes CI. The best first contribution is a new rule: one detector
function, one passing fixture, one failing fixture, tests. See
CONTRIBUTING for the full checklist.

## Community and support

| Channel | Best for |
|---|---|
| [GitHub Issues](https://github.com/techaurah/n8n-audit/issues) | Bugs and feature or rule requests (use the templates) |
| [GitHub Discussions](https://github.com/techaurah/n8n-audit/discussions) | Questions, ideas, show and tell |
| [SECURITY.md](SECURITY.md) | Vulnerabilities: report privately, never in a public issue |

## License

MIT. See [LICENSE](LICENSE).

## About TechAurah

TechAurah is an AI and software engineering company building AI
products, agents and intelligent automation for businesses in the USA,
UK, UAE, Canada, Australia and Europe. This tool grew out of real
client workflow audits: the rules are the checks we run by hand before
any workflow touches a client's leads.

We are available for AI engineering projects: https://techaurah.com
