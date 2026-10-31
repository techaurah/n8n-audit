# Contributing to n8n-audit

Thanks for helping make n8n workflows safer to run in production.

## Development setup (under 10 minutes)

```bash
git clone https://github.com/techaurah/n8n-audit
cd n8n-audit
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
```

No services, accounts or credentials are needed: everything runs offline
against fixture files.

## The best first contribution: a rule

This project grows one rule at a time. A complete rule PR contains:

1. A detector function in `src/n8n_audit/rules/<rule>.py`, registered in
   `rules/__init__.py`. A detector takes a `Workflow` and returns a list
   of `Finding` objects, nothing else. No I/O, no network, no globals.
2. A failing fixture in `fixtures/fail/<rule>.json` and a passing fixture
   in `fixtures/pass/<rule>.json`. Fixtures must use obviously fake data:
   never commit a real export or a real secret, not even your own.
3. Tests in `tests/rules/test_<rule>.py` covering the fixtures plus the
   edge cases your detector handles.
4. A section in `docs/rules.md` and a line in `CHANGELOG.md`.

Open a "New rule proposal" issue first so the failure class, severity
and detection approach can be agreed before you write code.

## Other good contributions

- Fixtures for edge cases of existing rules (new node types, odd exports).
- Clearer remediation text and better error messages.
- Documentation fixes and examples of CI usage.

## Pull request rules

- PRs must link an issue (`Closes #...`) and pass CI.
- Include test evidence in the PR: the command you ran and its result.
- Keep PRs small and single-purpose. A rule per PR, a fix per PR.
- Style: `ruff check src tests` must pass. Standard library only for the
  runtime package; new dependencies need a strong reason in the PR.

## Response rhythm

Issues are triaged at least weekly. Pull requests get a first human
response within a few days. If a claimed good first issue goes quiet for
two weeks, it may be unassigned so someone else can pick it up.

## Code of conduct

Participation is covered by the [Code of Conduct](CODE_OF_CONDUCT.md).
