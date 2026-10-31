# Security Policy

## Reporting a vulnerability

Report vulnerabilities privately through GitHub Security Advisories:
https://github.com/techaurah/n8n-audit/security/advisories/new

Please do not open a public issue for a security problem, and do not
include real secrets or real client workflow files in any report.

## Supported versions

Only the latest released version is supported with security fixes.
This project is pre-1.0, so that currently means the 0.1.x line.

## Notes on the tool itself

n8n-audit runs fully offline and only reads the workflow files you point
it at. It never sends workflow contents anywhere. Treat exported workflow
JSON as sensitive anyway: exports can contain the very secrets this tool
exists to catch, so audit them on machines you trust and never commit
unredacted exports of production workflows to a public repository.
