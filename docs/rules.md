# Rule reference

Every rule is deterministic: the same export always produces the same
findings, with no network calls and no AI involved. Each finding carries
a severity and a one-line remediation.

Severity guide:

| Severity | Meaning | Default CI effect |
|---|---|---|
| high | A real incident is a matter of time: exposed secrets, an open endpoint, silent failure | Fails the build (exit 1) |
| medium | A known production failure class with no guard in place | Reported; fails only with `--fail-on medium` |
| low | Maintainability and documentation debt (report-only rules) | Reported; fails only with `--fail-on low` |

## 1. `secrets-in-parameters` (high)

**Catches:** pasted secret material inside node parameters: OpenAI-style
API keys, GitHub and Slack tokens, AWS access key ids, private key
blocks, JSON web tokens, credential assignments inside code or text
(`api_key = ...`), and passwords embedded in URLs.

**Why it matters:** exported workflow JSON gets committed, screenshotted
and shared as templates. A key inside it has effectively been published.

**Fix:** move the secret into an n8n credential or an environment
variable and reference it; rotate the exposed value.

Expressions are not flagged: a parameter set to `={{ $env.MY_KEY }}` is
the correct pattern and passes. Sticky-note content is not scanned.

Fixtures: `fixtures/pass/secrets.json`, `fixtures/fail/secrets.json`.

## 2. `credentials-outside-store` (high)

**Catches:** nodes with no n8n credential attached whose parameters
fill a credential-shaped field directly: `apiKey`, `api_key`,
`clientSecret`, `accessToken`, `refreshToken`, `password`, `privateKey`,
`secretKey`, `authToken` and their close variants, at any depth.

**Why it matters:** the value is stored in plain text inside the
workflow, outside n8n's encrypted credential store, and travels with
every export.

**Fix:** create an n8n credential for the service, select it on the
node, and clear the raw field.

Empty values and `={{ ... }}` expressions are not flagged.

Fixtures: `fixtures/pass/credentials.json`,
`fixtures/fail/credentials.json`.

## 3. `webhook-without-auth` (high)

**Catches:** webhook trigger nodes whose `authentication` parameter is
missing, empty or `none`, with no credential attached to the node.

**Why it matters:** an unauthenticated webhook is a public write
endpoint. Anyone who finds the URL can inject leads, orders or events
into the workflow.

**Fix:** enable header auth, basic auth or JWT auth on the webhook
node and share the credential only with the calling system.

Fixtures: `fixtures/pass/webhooks.json`, `fixtures/fail/webhooks.json`.

## 4. `missing-error-workflow` (high)

**Catches:** workflows with no `settings.errorWorkflow` value.

**Why it matters:** without an error workflow, a failed execution is
silent. The lead or order the workflow existed to handle never lands
and nobody is told.

**Fix:** set an error workflow (Settings, Error Workflow) that alerts
a human and logs the failed execution.

Fixtures: `fixtures/pass/error-workflow.json`,
`fixtures/fail/error-workflow.json`.

## 5. `missing-deduplication` (medium)

**Catches:** workflows with a webhook or form trigger and no visible
deduplication pattern. This detector is a documented heuristic: a
workflow passes when any node name or parameter text mentions dedup,
duplicates, idempotency, processed ids or a similar check.

**Why it matters:** triggers deliver at least once, not exactly once.
Senders retry, users double-submit, providers redeliver, and each
redelivery becomes a duplicate email and a duplicate CRM record.

**Fix:** after the trigger, check a unique key (lead id, email,
submission id) against stored processed ids and stop early when it was
already handled.

Known limitation: a deduplication step with an unusual name and no
recognisable wording can be missed. Rename the node to say what it
does, which is also rule 7's advice.

Fixtures: `fixtures/pass/dedup.json`, `fixtures/fail/dedup.json`.

## 6. `http-without-retry` (medium)

**Catches:** HTTP Request nodes with none of: node-level
`retryOnFail: true`, an `options.retry` block, `options.retryOnFail`,
or an explicit node error setting (`onError`).

**Why it matters:** external APIs rate-limit (HTTP 429) and fail
transiently. With no retry and no error handling, a one-second blip
becomes permanently lost work.

**Fix:** enable Retry On Fail on the node (3 or more tries with a wait
between tries) or set explicit error handling.

Fixtures: `fixtures/pass/retry.json`, `fixtures/fail/retry.json`.

## 7. `default-node-names` (low, report-only)

**Catches:** in workflows with 8 or more nodes, nodes still carrying
default names such as `HTTP Request`, `Code1`, `IF`, `Set`, `Merge`
or `Webhook`.

**Why it matters:** default names make a production workflow
unreadable within months and turn every debugging session into
guesswork. Report-only: it never represents an incident risk.

**Fix:** rename the node to say what it does in this workflow.

Fixtures: `fixtures/pass/naming.json`, `fixtures/fail/naming.json`.

## 8. `missing-documentation` (low, report-only)

**Catches:** workflows containing no sticky-note node.

**Why it matters:** sticky notes are the only documentation that
travels with an exported workflow. Without one, the workflow explains
itself to nobody: not the next maintainer, not the client.

**Fix:** add at least one sticky note covering what the workflow does,
what triggers it and who owns it.

Fixtures: `fixtures/pass/documentation.json`,
`fixtures/fail/documentation.json`.
