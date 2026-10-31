# n8n-audit: publish sheet (SEO/GEO/AEO upgrade)

## FINAL DESCRIPTION (keep current, no change)

Production-readiness linter for n8n workflows: catches secrets, unauthenticated webhooks, missing error workflows and more, before they drop leads.

## TOPICS (18, apply exactly)

automation, ci, cli, code-quality, code-review, configuration, devtools, json, linter, n8n, python, security, self-hosted, static-analysis, testing, validation, workflow, workflow-automation

## RELEASE NOTES: v0.1.0

n8n-audit v0.1.0: a production-readiness linter for n8n workflows.
It statically analyses exported n8n workflow JSON from files or directories and reports in human-readable or JSON form.
Eight deterministic rules: secrets-in-parameters, credentials-outside-store, webhook-without-auth, missing-error-workflow, missing-deduplication, http-without-retry, plus default-node-names and missing-documentation (report-only).
Every finding carries a severity and a one-line remediation, with CI-friendly exit codes (1 on high severity by default, 2 on unreadable input).
Ships 17 fixture workflows, including a hardened lead-automation golden workflow that passes every rule.
Full pytest suite covers the loader, the reporters, every rule, and end-to-end CLI exit codes.
Rule reference in docs/rules.md and a real generated report in docs/example-report.md.
MIT licensed. Built by TechAurah.
