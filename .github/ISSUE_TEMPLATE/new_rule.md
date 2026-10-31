---
name: New rule proposal
about: Propose a new audit rule (the main way this project grows)
title: "[rule] "
labels: enhancement, needs-triage
---

**The failure class**
What production problem should the rule catch? Link a post-mortem, issue
or real incident if one exists.

**How to detect it statically**
What exactly appears (or is missing) in the exported workflow JSON?

**Severity and why**
high / medium / low, and what breaks when this fires in production.

**Remediation in one line**
The single action a workflow owner should take.

**Fixtures**
A PR for a new rule needs a passing fixture and a failing fixture under
`fixtures/`, plus tests. Say here if you plan to provide them.
