# Roadmap: n8n-audit

Where n8n-audit is going after v0.1.0. This is a plan, not a
promise: items land when they are built, tested, and reviewed, in
roughly this order.

## What v0.2 adds

- **More rules**, starting with the three most requested failure
  classes:
  - Credential expiry: credentials referenced by a workflow with
    no rotation or review signal.
  - Retry policy: HTTP and service nodes that can lose work
    because retries are missing or misconfigured beyond the
    current basic check.
  - Rate-limit handling: calls to known rate-limited APIs with
    no wait, queue, or backoff node in the path.
- More node-type coverage (queues, databases, AI agent nodes).
- SARIF output so findings land in GitHub code scanning.
- Per-rule ignore comments for deliberate, reviewed exceptions.

## Deliberately out of scope

- **It never runs, schedules, or modifies workflows.** It only
  reads exported workflow JSON and reports; fixing stays human.
- **Not an n8n plugin or editor integration** in this line of
  work. The CLI and CI come first; an integration is a later
  question, not a v0.2 item.
- **No live connection to your n8n instance**, and no telemetry.
  Exports are files; the tool works offline on purpose.

## How priorities are set

Priorities are set from GitHub issues and Discussions: open an
issue for concrete, actionable work (a new rule starts as an
issue with a failing example), and start a discussion for ideas
and questions.
