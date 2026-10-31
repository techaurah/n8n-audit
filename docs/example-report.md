# Example report

Real output from n8n-audit 0.1.0, generated against the fixtures in
this repository. Nothing below is edited.

## Passing workflow (exit code 0)

```console
$ n8n-audit fixtures/golden/lead-automation-hardened.json
Workflow: Lead Automation (Hardened) (fixtures/golden/lead-automation-hardened.json)
  OK: no findings

Summary: 1 workflow(s), 0 finding(s) (high=0, medium=0, low=0, info=0)
```

## Failing workflow, text format (exit code 1)

```console
$ n8n-audit fixtures/fail/secrets.json
Workflow: Lead Capture (Tutorial Copy) (fixtures/fail/secrets.json)
  [MEDIUM] missing-deduplication [node: Lead Webhook]: Workflow accepts webhook or form submissions but shows no deduplication pattern; redeliveries will be processed twice.
         Fix: Add a deduplication step after the trigger: check a unique key (lead id, email, submission id) against stored processed ids and stop early when it was already handled.
  [LOW] missing-documentation: Workflow contains no sticky-note documentation.
         Fix: Add at least one sticky note to the canvas explaining what the workflow does, what triggers it and who owns it.
  [HIGH] missing-error-workflow: Workflow has no error workflow configured in its settings.
         Fix: Set an error workflow in the workflow settings (Settings > Error Workflow) that alerts a human and logs the failed execution.
  [HIGH] secrets-in-parameters [node: Enrich Lead]: Possible credential assignment in text pasted into parameter 'jsCode'.
         Fix: Move the secret into an n8n credential or an environment variable and reference it; rotate the exposed value, it has left the building.
  [HIGH] secrets-in-parameters [node: Notify Provider]: Possible OpenAI-style API key pasted into parameter 'headerParameters.parameters[0].value'.
         Fix: Move the secret into an n8n credential or an environment variable and reference it; rotate the exposed value, it has left the building.

Summary: 1 workflow(s), 5 finding(s) (high=3, medium=1, low=1, info=0)
```

## Failing workflow, JSON format (exit code 1 with --fail-on medium)

The retry finding below is medium severity, so it only fails the run
when the threshold is lowered to medium.

```console
$ n8n-audit --format json --fail-on medium fixtures/fail/retry.json
{
  "summary": {
    "workflows": 1,
    "findings": 2,
    "by_severity": {
      "info": 0,
      "low": 1,
      "medium": 1,
      "high": 0
    }
  },
  "results": [
    {
      "workflow": "Rate Fetcher",
      "source": "fixtures/fail/retry.json",
      "findings": [
        {
          "rule": "http-without-retry",
          "severity": "medium",
          "node": "Fetch Exchange Rates",
          "message": "HTTP request node has no retry on fail and no explicit error handling; a transient API error will drop this work.",
          "remediation": "Enable 'Retry On Fail' on the HTTP node (3 or more tries with a wait between tries) or set explicit error handling for the node."
        },
        {
          "rule": "missing-documentation",
          "severity": "low",
          "node": null,
          "message": "Workflow contains no sticky-note documentation.",
          "remediation": "Add at least one sticky note to the canvas explaining what the workflow does, what triggers it and who owns it."
        }
      ]
    }
  ]
}
```
