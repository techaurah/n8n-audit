# AGENTS.md

Instructions for AI coding agents (and humans skimming) working in this repo.

## Layout

- `src/n8n_audit/` is the whole product. Standard library only at runtime.
- `src/n8n_audit/rules/` holds one module per rule. A rule is a pure
  function `detect(workflow) -> list[Finding]` registered in
  `rules/__init__.py` (`ALL_RULES`).
- `fixtures/` holds exported-workflow JSON used by tests: `golden/` (must
  always pass every rule), `pass/` and `fail/` (one file per rule).
- `tests/` mirrors the package: `tests/rules/test_<rule>.py` per rule.

## Commands

- Install: `pip install -e ".[dev]"`
- Test: `pytest -q`
- Lint: `ruff check src tests`
- Run: `n8n-audit fixtures/golden/lead-automation-hardened.json`

## Conventions

- Never add a runtime dependency without maintainer agreement.
- Never commit real workflow exports, real credentials or real client
  data, including in fixtures and test output. Fixture secrets are
  obviously fake demo strings by design.
- The golden fixture must stay green under every rule. If a new rule
  fails it, either the rule or the fixture is wrong; fix deliberately and
  say which in the PR.
- Every new rule needs: detector, pass fixture, fail fixture, tests,
  a `docs/rules.md` section, a CHANGELOG entry.
- Exit codes are a public contract: 0 clean, 1 findings at or above
  `--fail-on`, 2 unreadable input. Do not change them casually.
