# Watson AI Wrapper Architecture Review and Future-Proof Recommendations

**Reviewed document:** `watson-ai-wrapper-architecture.md`  
**Review date:** 2026-07-20  
**Decision:** The implementation is a complete, well-tested MVP and a sound production candidate after environment-specific security, provider-contract, and operational acceptance checks. The recommendations below are future-proofing improvements, not a conclusion that the current code is incomplete.

## Executive Summary

The proposal and implementation form a good architecture for adding optional AI diagnostics to an existing Tekton flow. Its strongest decision is the fail-safe compatibility boundary: successful statuses and all enrichment failures preserve the original pipeline result, while AI diagnostics stay outside the mechanism that determines pipeline success or failure. The standalone Go CLI, standard-input/standard-output contract, external prompt packs, bounded HTTP calls, secret handling, and test strategy are sound and already implemented.

The codebase implements substantially more hardening than the original proposal alone makes obvious. It already includes strict input parsing, exact byte preservation on success/fallback, runtime model selection by exact ID, layered redaction, prompt-root confinement, HTTPS-only endpoints, redirect refusal, bounded input/request/response sizes, private output-file replacement, structured logging, layered timeouts, transient retries, IAM token caching, prompt-injection instructions, fake-service integration tests, and an opt-in scored live Watson test.

The main remaining future-proofing opportunities are:

1. Three sequential model calls are deliberately used for every failure. This may improve separation and diagnosis quality, but it also increases latency, cost, rate-limit exposure, and fallback probability. The correct long-term strategy should be selected through evaluation rather than assumed.
2. The final model response is free-form text at runtime. Prompt rules and the live E2E scorer check format, evidence, known misleading advice, and the 180-word limit, but these checks do not run on each production response.
3. Pipeline logs are untrusted external content. The implementation has layered regex redaction, size limits, prompt-injection instructions, and safe logging, but organization-specific DLP, data-egress approval, retention, and residency policy remain deployment responsibilities.
4. The intentionally conservative rule treats any valid document that is not exact success as failure. That matches the documented contract, but a future upstream schema with new states would benefit from explicit versioning or an eligibility policy.
5. A small `ChatClient` interface already isolates orchestration tests, but configuration, message types, authentication, and package names remain Watson-specific. Further provider-neutralization is useful only if a second provider or internal gateway is a realistic requirement.
6. A few configuration fields are deliberately reserved and accurately documented as inactive. This is configuration debt, not hidden behavior, and can be removed or implemented when the corresponding feature is prioritized.

The best path is not a rewrite. Keep the current CLI, package boundaries, exact pass-through behavior, Watson adapter, prompt packs, and tests. Add runtime response validation, explicit contract/eligibility policy, production telemetry, and deployment governance first. Benchmark a one-call strategy against the implemented three-call strategy before changing orchestration. Introduce broader provider abstraction, parallel map/reduce, or a shared service only when a demonstrated requirement justifies the extra complexity.

## Overall Assessment

| Area | Rating | Assessment |
| --- | ---: | --- |
| Compatibility with the existing pipeline | 5/5 | Excellent. The CLI post-processor and exact fallback minimize Tekton changes. |
| Failure isolation | 5/5 | Excellent. AI is not allowed to determine the command or wrapper exit status. |
| Code organization and testability | 4/5 | Good package boundaries, interfaces, fixtures, and fake HTTP tests. |
| Latency and cost efficiency | 2.5/5 | Three sequential calls are intentional and bounded, but no evaluated lower-call strategy is available. |
| Output reliability | 3/5 | Prompts and live E2E checks enforce useful quality rules; production responses still lack runtime schema/grounding validation. |
| Security and privacy | 3.5/5 | Strong code-level baseline: redaction, size limits, prompt-injection instructions, HTTPS, redirect refusal, secret-safe logs, and path protections. Organization DLP/egress governance remains. |
| Provider and model portability | 3/5 | Runtime exact-ID selection and `ChatClient` abstraction exist; config, message types, and auth remain Watson-specific. |
| Operability and governance | 3/5 | Structured logs, version metadata, retries, layered time/size budgets, E2E scoring, and release guidance exist. Metrics/traces, cost quotas, and automated lifecycle alerts do not. |

**Conclusion:** This is more than a proof-of-concept: it is a complete MVP with a coherent safety contract and meaningful automated verification. Production approval still depends on real Watson contract testing and the organization's privacy, network, quota, monitoring, and release requirements. The target architecture in this document is an evolution path, not a replacement mandate.

## Implementation Reconciliation

This section distinguishes what is already present in the repository from what is partial or not implemented. It is based on `README.md`, all Go packages, shipped prompt/config assets, shell integration, and tests.

Primary repository references: [implementation guide](README.md), [CLI boundary](cmd/ai-status-wrapper/main.go), [status parser](internal/aistatus/status.go), [enrichment orchestration](internal/aistatus/wrapper.go), [configuration](internal/config/config.go), [log preparation](internal/logprep), [prompt loader](internal/prompts/loader.go), [Watson client](internal/watsonx/client.go), and [live E2E scorer](cmd/ai-status-wrapper/real_e2e_test.go).

### Already implemented

| Capability | Implementation evidence |
| --- | --- |
| Standalone integration boundary | Independent Go 1.23 module with no third-party modules; CLI uses `stdin`/`stdout`; optional POSIX launcher and Tekton examples are provided. |
| Exact fail-safe behavior | Success, invalid input, configuration/auth/provider/timeout failures return original bytes; only CLI/I/O failures use nonzero process exits. |
| Strict status parsing | Required fields and types, top-level object, single JSON value, failure log fields, and integer parsing are validated in `internal/aistatus/status.go`. |
| Minimal mutation | Successful enrichment changes only `error_message` semantically and preserves unknown fields; tests compare all remaining fields. |
| Safe stream and file output | Protocol output stays on `stdout`; logs stay on `stderr`; file output uses a temporary `0600` file plus rename and does not overwrite a symlink target. |
| Input and body bounds | CLI input is capped at 10 MiB; prompt files at 1 MiB; logs are reduced; Watson request/response and IAM response sizes are bounded. |
| Layered redaction | Baseline credential patterns, config patterns, and an optional capture-compatible regex file are combined before external calls. Original fallback bytes remain unchanged. |
| Prompt hardening | System prompts explicitly treat logs/status as untrusted evidence; prompt loading is deterministic, size-limited, traversal-safe, and symlink-confined. Missing roles/placeholders cause fallback. |
| Network/auth hardening | HTTPS-only absolute endpoints, normal TLS verification, redirect refusal, environment-only API key, IAM exchange, token expiry margin, and process-local token caching. |
| Timeout and retry controls | Overall context timeout, per-request HTTP timeout, provider generation time limit, transient-only retries, exponential backoff, and retry-count bounds. |
| Model and prompt selection | Exact model selection through `WATSONX_MODEL_ID`, allowlisted against configured models; runtime project override; pipeline/prompt-version selection; deterministic few-shot loading. |
| Partial provider abstraction | `aistatus.Processor` consumes the small `watsonx.ChatClient` interface, so orchestration tests are independent of HTTP and IAM. |
| Logging and build identity | `log/slog` levels, secret-safe attributes, model/pipeline/prompt metadata, `--version`, build-time version injection, and documented checksum/release practices. |
| Automated verification | Unit/integration tests with fake IAM/Watson servers, status fixtures, exact-pass-through tests, race/vet/build commands, and opt-in live Watson E2E scoring. |
| Live quality checks | The opt-in E2E scorer checks field preservation, changed/prefixed message, evidence overlap, actionability, fixture-specific diagnoses, known misleading guidance, and the 180-word limit. |

### Partially implemented

| Capability | Current boundary |
| --- | --- |
| Output validation | Fresh prompts request JSON and live E2E tests score final text, but production runtime accepts any non-empty final model text and adds the `AI analysis:` prefix. |
| Model portability | Exact runtime model-ID selection already avoids relying solely on list index. The default remains the first/configured index, and provider capability metadata/lifecycle automation is absent. |
| Provider portability | The chat interface isolates orchestration, but its messages and all concrete config/auth/client code are Watson-specific. |
| Evaluation gate | Four realistic synthetic failure fixtures and deterministic reliability checks exist. Privacy canaries, prompt-injection fixtures, broader failure coverage, and automated staging/release execution can be added. |
| Observability | Structured logs include lifecycle and selected model/prompt context. Metrics, traces, token/cost reporting, correlation IDs, and reason-coded counters are not emitted. |
| Resource budgeting | Input, prompt, context, generation, body, HTTP, and overall time limits exist. There is no per-run call budget setting, token billing budget, concurrency budget, or daily quota. |
| Artifact/release controls | Version embedding, checksum instructions, OS/architecture guidance, and a release checklist are documented; signed artifacts and an automated release workflow are not included in this repository. |
| Large-log handling | Selection-based reduction is active and tested. True chunk-by-chunk analysis is intentionally reserved; its config fields are currently inactive. |

### Not implemented

- Explicit input/output schema-version fields and unknown-version handling.
- Runtime structured final-response schema validation and evidence-quote verification.
- Organization-specific DLP, data-egress allowlists, retention, and data-residency enforcement.
- Metrics/OpenTelemetry, cost/quota controls, and shared-service circuit breaking.
- `Retry-After` handling and randomized retry jitter.
- Automated model deprecation/capability monitoring.
- Adaptive one-call versus map/reduce orchestration.
- PR and CD prompt packs; only `sync/v1` is shipped.
- A shared/asynchronous enrichment service, which is not needed for the current CLI scope.

### Verification performed for this audit

The following local checks passed on 2026-07-20:

```text
go test ./...                  PASS
go test -race ./...            PASS
go test -cover ./...            PASS; package coverage 73.9% to 86.5%
go vet ./...                   PASS
go list -m all                 PASS; only ai-status-wrapper
sh -n ai-status-wrapper.sh     PASS
gofmt diff check               PASS; no formatting drift
```

The credentialed `TestRealWatsonEndToEndScore` was not executed during this audit because it requires `RUN_WATSONX_E2E=1`, an IBM API key, a project ID, network access, model quota, and potential cost. The test itself and its deterministic scoring helpers were reviewed. Production acceptance should run it in the approved environment.

## What the Proposal Gets Right

### 1. Correct trust boundary around the pipeline result

The AI wrapper is an optional enrichment layer, not the authority for pipeline success. Returning original bytes on success, invalid input, configuration failure, timeout, authentication failure, or model failure is the correct reliability contract.

This guarantee should remain non-negotiable in every future version.

### 2. Minimal integration surface

Reading one JSON document from `stdin` and writing one JSON document to `stdout` is easy to introduce, test, remove, or replace. Keeping diagnostic logs on `stderr` prevents corruption of the JSON pipeline variable.

### 3. Standalone, cohesive implementation

The current packages separate status parsing, orchestration, prompt loading, log preparation, configuration, IAM, and Watson communication. The thin CLI is also a good boundary. This structure can be evolved without changing the Tekton call site.

### 4. Defense-in-depth baseline

The implementation keeps credentials out of configuration, requires HTTPS, refuses HTTP redirects, bounds request and response sizes, redacts logs, applies timeouts, and retries only transient classes of HTTP errors. These are valuable controls.

### 5. Good initial verification

At review time, `go test ./...` passes for every package. Statement coverage is approximately 73.9% to 86.5% by package. Tests verify exact pass-through, fallback behavior, redaction, retry behavior, prompt selection, and one-IAM/three-chat orchestration using local fake services.

## Recommended Hardening and Future-Proofing

### High priority: Add runtime validation for the final diagnosis

The production path accepts the final model message as developer-facing text as long as it is non-empty, trimming it and applying the `AI analysis:` prefix when needed. This is not completely unguarded: the final prompt requires explicit evidence and a maximum of 180 words, and the opt-in live E2E scorer checks evidence overlap, actionability, fixture-specific accuracy, known misleading advice, and the word limit. However, those deterministic checks are test-time controls and do not validate each production response.

Use a strict response schema when the selected model/deployment supports it. Current IBM watsonx SDK documentation exposes `response_format` with `json_object` and `json_schema`, including strict schema adherence. See [IBM watsonx.ai chat parameter schema](https://ibm.github.io/watsonx-ai-python-sdk/fm_schema.html). If the selected model lacks strict-schema support, parse a JSON response and apply the same local validator; otherwise retain the current text mode with deterministic length and safety checks.

Recommended internal contract:

```json
{
  "schema_version": "diagnosis.v1",
  "summary": "The deployment failed because the service account cannot update deployments.",
  "category": "permission_denied",
  "confidence": 0.91,
  "evidence": [
    {
      "source": "stderr",
      "quote": "deployments.apps is forbidden",
      "line_hash": "sha256:..."
    }
  ],
  "likely_root_cause": "The Tekton service account lacks the required RBAC permission.",
  "recommended_actions": [
    "Grant the minimum required update permission for deployments.apps.",
    "Re-run kubectl auth can-i using the pipeline service account."
  ],
  "follow_up_checks": [
    "Confirm the RoleBinding namespace matches the deployment namespace."
  ]
}
```

Validate deterministically before mutation:

- Reject unknown schema versions and missing required fields.
- Cap every field and array length.
- Allow only a controlled category enumeration.
- Require each evidence quote to exist in the sanitized evidence bundle.
- Reject shell control characters, terminal escape sequences, and unsafe markup.
- Reject output whose recommendation is unsupported by the supplied evidence.
- Render the validated structure into `error_message` for the current v1 compatibility mode.
- Return the original JSON if validation fails.

Do not expose raw provider response types to the status-mutation layer.

### Medium priority: Evaluate an adaptive call strategy

The implementation intentionally calls the model for `stderr`, then `stdout`, then final synthesis. This provides source isolation and lets the final call work from two focused analyses. With retries, however, the number of external requests can grow, and each required call becomes another point at which otherwise useful enrichment is discarded.

Candidate adaptive strategy to benchmark against the current design:

1. Sanitize and extract a bounded evidence bundle from status metadata, `stderr`, and `stdout` in deterministic code.
2. Send that combined evidence in one structured diagnosis call for ordinary failures.
3. If the input is too large, split it into bounded chunks and analyze only the selected chunks.
4. Run chunk-analysis calls concurrently with a small configured limit.
5. Run one final reducer call only when multiple chunk analyses actually exist.

This could change the common case from three calls to one while preserving a hierarchical option for unusually large logs. Do not make this change based on call count alone. Compare diagnostic accuracy, unsupported-claim rate, latency, token usage, throttling, and fallback rate on the existing E2E corpus plus a larger sanitized corpus. Keep the current three-call strategy if it produces materially better outcomes within the accepted latency/cost budget. Record the selected strategy (`three_stage`, `single`, `map_reduce`, or `deterministic_only`) in telemetry.

### Contract decision: Define eligibility for future status states

The current rule treats every valid combination other than exact success as a failure. This is deliberate, documented, and tested; it should not be changed without agreement from the upstream `capture-error` contract. It is conservative for diagnosing any inconsistent status but would not be conservative for external data disclosure if a future producer introduced intermediate, cancelled, or otherwise non-failure states using the same shape.

When the upstream schema gains additional states, introduce a classification/eligibility enum such as:

```text
ConfirmedSuccess  -> exact byte pass-through; no external call
ConfirmedFailure  -> eligible for enrichment
UnknownState      -> exact byte pass-through; no external call
InvalidDocument   -> exact byte pass-through; no external call
```

Define confirmed failure explicitly in a versioned capture-error schema. Until such a contract change is approved, preserve the implemented four-field rule and document the external-enrichment consequence. A deployment-level eligibility policy can additionally limit which pipelines/repositories may send failure logs without redefining command success.

### High priority: Complete deployment-level data governance

Logs can contain credentials, personal data, internal URLs, source snippets, customer information, and attacker-controlled prompt text. OWASP specifically recommends separating untrusted content, constraining model behavior, validating expected output, filtering input/output, and adversarial testing. See [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) and [OWASP LLM05:2025 Improper Output Handling](https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/).

The implementation already applies baseline/config/file redaction, bounds inputs and provider bodies, refuses redirects, avoids content logging, and tells the model to treat supplied content as untrusted evidence. Add the controls that require organization-specific policy:

- Default-deny enrichment for repositories or pipeline classes not approved for external AI processing.
- Allow region, provider, project, and model only through an administrative allowlist.
- Redact known secrets and high-risk identifiers with both deterministic patterns and organization DLP rules.
- Drop binary data, environment dumps, private keys, authorization headers, cookies, signed URLs, and high-entropy token-like strings.
- Preserve the existing untrusted-evidence prompt rules and strengthen structured boundaries where supported.
- Never rely on the system prompt as the security control.
- Reject or flag model output that repeats redacted values or contains new URLs/commands not supported by evidence.
- Define retention, audit, incident-response, and data-residency requirements with the security/privacy owner.
- Add adversarial fixtures containing instructions such as “ignore previous instructions” and fake system messages.

The wrapper does not execute model recommendations, which substantially limits impact. Preserve that non-agentic design.

### Production acceptance: Verify the live Watson chat contract

The proposal and current client send `parameters.max_new_tokens`. The repository already contains an opt-in live Watson E2E test, and the README documents observed live output, so the integration is not limited to mocks. Current IBM chat SDK documentation also describes `max_tokens` and `max_completion_tokens` for chat requests, while `max_new_tokens` is associated with text generation. Treat this as a version/model compatibility check, not as a confirmed defect in the current endpoint.

Before production:

- Confirm the exact REST schema for the targeted watsonx deployment and API version.
- Run the existing live E2E test in a controlled staging/release job and add a focused assertion for request-parameter behavior where the service exposes it.
- Add structured response-format capability detection per model/deployment.
- Pin a supported API version and schedule an upgrade check.
- Continue testing every approved model profile with the existing real E2E flow before changing defaults.

### Low priority: Resolve deliberately reserved configuration

The repository documentation accurately identifies several forward-looking fields that are validated but do not drive behavior:

- `prompting.metrics_label` is not emitted.
- `http.body_warning_bytes` does not generate warning telemetry.
- `chunking.chunk_size_tokens` and `chunk_overlap_tokens` do not control chunk calls.
- `fallback` booleans cannot change the mandatory fallback behavior.

Because this status is clearly documented, it is not hidden or incorrect implementation behavior. Nevertheless, active-only configuration is easier to operate. Either implement the reserved fields when their feature is prioritized or remove them in a versioned config migration. Mandatory fallback should remain code policy rather than a configurable boolean. If fields are removed, reject them with a clear migration message instead of silently ignoring them; the current config decoder already rejects unknown fields.

## Future-Proof Target Architecture

Continue using the implemented modular CLI. The diagram below is an evolution of the existing stages, adding explicit eligibility and runtime response validation. It does not require a service or a new deployment topology.

```text
capture-error JSON
       |
       v
Input Adapter + Size Limit
       |
       v
Versioned Status Parser
       |
       +--> success / unknown / invalid --> exact original bytes
       |
       v
Confirmed Failure Policy
       |
       +--> enrichment disabled / budget exhausted --> exact original bytes
       |
       v
Sanitizer + DLP + Evidence Extractor
       |
       v
Strategy Selector
       |
       +--> deterministic known-failure rule
       |
       +--> current three-stage flow or evaluated one-call flow
       |
       +--> bounded parallel map + one reduce (large input only)
       |
       v
Schema Validator + Evidence Grounding Check
       |
       +--> invalid / low confidence --> exact original bytes
       |
       v
Compatibility Writer
       |
       +--> v1: update only error_message
       +--> v2 opt-in: add versioned ai_analysis object
       v
Final status JSON
```

### Stable core interfaces

The current `watsonx.ChatClient` interface already separates orchestration tests from HTTP/IAM. If provider portability becomes a real requirement, move provider-specific messages, request fields, and authentication behind a provider-neutral domain interface:

```go
type DiagnosisProvider interface {
    Diagnose(ctx context.Context, request DiagnosisRequest) (Diagnosis, ProviderMetadata, error)
}

type EvidencePreparer interface {
    Prepare(ctx context.Context, status StatusEnvelope) (EvidenceBundle, error)
}

type DiagnosisValidator interface {
    Validate(d Diagnosis, evidence EvidenceBundle) error
}
```

`DiagnosisRequest`, `Diagnosis`, and `EvidenceBundle` would belong to a provider-neutral domain package. A Watsonx adapter could translate them into IBM chat messages and response-format parameters. Future adapters could support another hosted provider, an internal gateway, or an on-premises model without changing parsing, safety policy, or status mutation.

Avoid building a general plugin framework now. The existing small chat interface is sufficient for the current single-provider scope. Introduce broader domain types only when runtime response validation needs them or a second provider is actually required.

### Model profiles instead of numeric selection

The implementation already supports exact runtime selection through `WATSONX_MODEL_ID`, validates that ID against the configured allowlist, and uses the numeric index only as the config/default selection. This is safer than relying only on an index. Reordering still changes the default when `selected` is omitted or index-based, and direct provider IDs still couple deployment configuration to provider lifecycle.

If multiple environments, fallback models, or provider migration become important, add a stable logical profile:

```yaml
runtime:
  provider: watsonx
  model_profile: ci-diagnosis-default

model_profiles:
  ci-diagnosis-default:
    provider_model_id: "<current-approved-model-id>"
    response_schema: diagnosis.v1
    max_input_tokens: 24000
    max_output_tokens: 900
    supports_strict_json_schema: true
```

Map the logical profile to the approved model per environment. Validate capabilities in the existing live E2E release/smoke test. IBM states that multitenant foundation models are updated and deprecated over time, with limited notice periods for withdrawal, so model lifecycle cannot safely be treated as static configuration. See [IBM foundation model lifecycle](https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/fm-model-lifecycle.html?context=wx).

Recommended lifecycle controls:

- Maintain primary and fallback model profiles, each separately evaluated.
- Do not silently switch models inside one invocation unless both pass the same evaluation gate and the switch is observable.
- Run a scheduled availability/capability smoke test.
- Open an operational alert when a deprecation notice appears.
- Record the provider, resolved model/deployment ID, prompt version, and schema version with every enrichment metric.

### Version the input and output contracts

The existing parser is strict about required fields and types and preserves unknown fields, but the input has no explicit schema version. Add one only in coordination with the upstream collector:

```json
{
  "schema_version": "capture-status.v1",
  "success": false,
  "status": "failed",
  "exit_code": 1,
  "wrapper_exit_code": 1,
  "output": {
    "stdout": "...",
    "stderr": "..."
  }
}
```

During migration, support the current unversioned shape as `legacy.v0` with a strict compatibility parser. Unknown future versions must pass through without external enrichment.

For output, keep two modes:

- `compat-v1` (default): change only `error_message` after validation.
- `analysis-v2` (opt-in): also add a structured `ai_analysis` object with `schema_version`, category, confidence, evidence references, actions, provider/model profile, and prompt version.

Do not include secrets or full prompts/logs in metadata. If downstream consumers perform strict schema validation, enable `analysis-v2` only after contract tests confirm compatibility.

## Evidence Preparation Improvements

The implemented first/signal/last reduction is bounded and tested to retain representative failure/end evidence. It is a reasonable dependency-free control, but it is not a model-specific tokenizer or full root-cause extractor. A four-bytes-per-token estimate can be inaccurate across models and languages, and selecting signal lines in source order can omit later evidence once the signal budget is exhausted.

Recommended evidence bundle:

- Command metadata and exit/failure fields.
- Last non-repeated error block from `stderr`.
- A small window before and after high-signal lines.
- Deduplicated repeated lines with occurrence counts.
- Structured recognizers for Kubernetes, Go test, compiler, HTTP, IAM/RBAC, YAML, image-pull, timeout, and shell failures.
- Truncation metadata and original byte counts.
- Stable hashes for evidence lines used to ground the response.
- A provider-specific token counter when available, with a conservative byte ceiling as the final protection.
- UTF-8-safe truncation; the current final byte slice can split a multi-byte character at an exact limit, so add non-ASCII boundary tests before broad multilingual use.

Run deterministic recognizers before the model. For well-known exact patterns, either return a reviewed deterministic diagnosis or include the recognized category as evidence. Do not allow a rule to change pipeline success.

Also account for the complete rendered message, not only selected log text. Current context validation compares configured input/output budgets with the declared model context, while actual requests also contain system/user templates, response-pattern messages, few-shot examples, status metadata, and JSON/message overhead. The hard request-body limit still provides a byte-level fallback, but a provider-aware token calculation would make context budgeting more accurate.

The repository intentionally has no third-party Go modules. Do not add a tokenizer dependency casually. If that constraint remains mandatory, use conservative byte/headroom calculations and provider-reported token usage for monitoring, or implement any tokenizer change only through a separately reviewed dependency decision.

## Reliability, Cost, and Performance Controls

### Time budgets

The wrapper already has an overall context deadline, a per-request HTTP timeout, and a provider generation time limit. Preserve those layers. A possible refinement is to derive explicit per-stage budgets from the remaining overall deadline so early calls cannot consume nearly all time intended for final synthesis. The Tekton guidance already instructs operators to keep the wrapper timeout shorter than the enclosing step timeout.

### Retries

The implementation already retries network errors, `429`, and `5xx`, avoids retrying ordinary `4xx`, uses exponential backoff, caps retry count, and remains bounded by the overall context deadline. Incremental improvements are:

- Honor `Retry-After` for `429` and applicable service responses.
- Add bounded jitter to exponential backoff.
- Retry only idempotent inference requests with the same request identifier.
- Optionally expose a retry-time sub-budget within the existing overall deadline.
- Record retry cause and count without logging payloads.

### Circuit breaker and budgets

For a one-document CLI, a process-local circuit breaker has little value. Enforce a deployment-level disable switch and, if a shared service is introduced, add a provider/region circuit breaker there.

The code already has a 10 MiB input cap, prompt/log/context/generation budgets, HTTP body caps, retry bounds, and an overall deadline. Additional operational limits to consider are:

- Maximum enrichments per pipeline run.
- Maximum calls per enrichment.
- Maximum input and output tokens/bytes.
- Daily or monthly spend/quota.
- Maximum concurrent calls in map/reduce mode.

When a limit is reached, return the original JSON and emit a reason-coded metric.

## Observability Without Log Leakage

Emit metrics or OpenTelemetry spans with bounded labels only. Do not use repository names, commands, error messages, or model output as labels.

Minimum measures:

| Measure | Purpose |
| --- | --- |
| `enrichment_attempts_total` | Adoption and load |
| `enrichment_success_total` | Useful completion rate |
| `enrichment_fallback_total{reason}` | Config, auth, timeout, provider, schema, privacy, budget, or unknown-state failures |
| `enrichment_duration_seconds` | Pipeline overhead |
| `provider_requests_total{operation,status_class}` | Provider reliability |
| `provider_retry_total{reason}` | Throttling and instability |
| `input_bytes` / `selected_evidence_bytes` | Reduction effectiveness |
| `prompt_tokens` / `completion_tokens` when supplied | Cost monitoring |
| `diagnosis_category` and confidence bucket | Quality mix using a bounded enumeration |

Use request/correlation IDs in logs and provider headers where supported. Record resolved model profile, prompt version, response schema, wrapper build version, and strategy. Never record raw logs, prompts, credentials, or unrestricted model responses in routine telemetry.

## Evaluation and Release Gates

The implemented live end-to-end score is a meaningful smoke/quality test, not merely a proposal. It already makes field preservation and fixture-specific reliability hard requirements independent of the configurable total-score threshold. Its deterministic checks cover known misleading `yq` advice, Tekton step isolation, unsupported Go speculation, four failure categories, and the 180-word limit. It remains opt-in, uses four synthetic failure fixtures, and does not validate every production response.

Create a versioned, sanitized evaluation corpus with representative and adversarial failures. Each case should contain expected categories, required evidence, forbidden claims, acceptable action sets, and privacy markers.

Retain the existing checks and extend release gates with:

1. Preserve the existing deterministic exact-pass-through, field-preservation, redaction, path, retry, and reliability tests.
2. Add runtime-schema validator tests for every enriched output once structured diagnosis is implemented.
3. Add privacy tests proving canary secrets and representative PII patterns never reach the fake provider.
4. Add prompt-injection and malicious-log fixtures.
5. Expand golden-category accuracy and unsupported-claim measurement beyond the four shipped failure fixtures.
6. Add actionability review on a sample by maintainers.
7. Add latency, call-count, token, and cost budgets to the controlled live run.
8. Run the existing live E2E suite as a staging/release contract check for each approved model.
9. Use shadow-mode comparison before a materially different prompt/model becomes default when operationally feasible.
10. Preserve rollback by binary version and prompt pack; add a deployment-level disable switch/model-profile rollback if required by operations.

An LLM-as-judge score may be one signal, but deterministic safety/contract checks must be mandatory and independent of that score.

## Deployment Evolution

### Phase 1: Complete production acceptance and runtime validation

Recommended next, building on the existing CLI:

- Keep the current Tekton integration, exact fallback contract, redaction, prompt isolation, network controls, and test suite.
- Run the existing live E2E suite for the actual production model, API version, region, and network path.
- Add runtime schema/length/safety validation and evidence grounding for the final response.
- Complete organization-specific egress, retention, residency, and secret/PII policy.
- Add adversarial/privacy fixtures and reason-coded metrics.
- Decide whether future upstream states require versioned eligibility; do not change the current classifier unilaterally.

This gives the largest remaining reliability improvement with the smallest deployment change.

### Phase 2: Evaluate call strategy and model profiles

After collecting quality, latency, token, and fallback data:

- Benchmark the current three-stage flow against a single structured call.
- Keep the better strategy per accepted quality/latency/cost targets rather than assuming fewer calls are always better.
- Add logical model profiles if environments, fallbacks, or lifecycle management need an alias above exact `WATSONX_MODEL_ID` selection.
- Implement token-aware chunk selection and bounded parallel analysis only for failures whose evidence cannot fit the selected strategy.

Do not implement chunking merely because fields already exist in configuration; they are already documented as reserved.

### Phase 3: Optional shared enrichment service

Consider a service only if scale or operations justify it—for example, high call volume, centralized governance, shared token caching, provider circuit breaking, asynchronous enrichment, or multiple CI systems.

The pipeline-facing CLI should remain as the compatibility adapter. It can call the service with a short deadline and return original input on service failure. If asynchronous results are acceptable, publish enrichment separately rather than delaying the command-status path. Do not replace the simple CLI with mandatory infrastructure before those needs are demonstrated.

## Suggested Package Layout

```text
cmd/ai-status-wrapper/          # CLI adapter only
internal/status/                # versioned parse, classify, compatibility write
internal/policy/                # eligibility, egress, budgets, strategy selection
internal/evidence/              # sanitize, DLP, recognize, reduce, ground
internal/diagnosis/             # provider-neutral request/result/schema validation
internal/providers/watsonx/     # IBM auth and chat adapter
internal/prompts/               # versioned prompt assets and rendering
internal/telemetry/             # bounded logs, metrics, traces
internal/evaluation/            # reusable deterministic evaluation helpers
config/                         # active settings only
testdata/                       # contract, privacy, adversarial, and quality fixtures
```

Package names should reflect business responsibility rather than a specific model API, except inside the provider adapter.

## Optional Future Configuration Shape

```yaml
contract:
  input_versions: ["legacy.v0", "capture-status.v1"]
  output_mode: "compat-v1"

enrichment:
  enabled: true
  confirmed_failure_only: true
  strategy: "adaptive"
  overall_timeout_ms: 30000
  max_provider_calls: 3
  min_confidence: 0.65

policy:
  approved_pipeline_types: ["sync"]
  deny_on_possible_secret: true
  max_log_bytes_before_redaction: 10485760
  max_evidence_bytes: 131072

runtime:
  provider: "watsonx"
  model_profile: "ci-diagnosis-default"

model_profiles:
  ci-diagnosis-default:
    provider_model_id: "<approved-model-id>"
    response_schema: "diagnosis.v1"
    supports_strict_json_schema: true
    max_input_tokens: 24000
    max_output_tokens: 900

provider:
  watsonx:
    url: "https://us-south.ml.cloud.ibm.com"
    api_version: "<validated-api-version>"
    project_id_env: "WATSONX_PROJECT_ID"
    api_key_env: "WATSONX_API_KEY"
    iam_token_url: "https://iam.cloud.ibm.com/identity/token"

telemetry:
  metrics_enabled: true
  traces_enabled: true
  include_content: false
```

This is an optional future shape, not a claim that the current configuration is invalid. The current loader already applies defaults, rejects unknown fields, validates model/context/HTTP/chunk limits, and accepts runtime project/model overrides. Secrets must remain environment/secret-manager values. If this shape is adopted, use an explicit versioned migration and keep only active settings.

## Prioritized Action Plan

### Highest priority

1. Run the existing live Watson E2E suite against the exact production model/API/region and include it in the controlled release process.
2. Define a versioned internal `Diagnosis` schema and add strict runtime output validation, length enforcement, and evidence grounding.
3. Complete the organization-specific privacy/egress/retention/residency review and add adversarial/privacy fixtures.
4. Emit reason-coded latency, fallback, request, retry, model, prompt, and strategy metrics without content leakage.
5. Confirm whether the upstream status contract can ever produce non-failure states that are not exact success; version eligibility only if that contract expands.

### Next, based on measurements

1. Expand the existing sanitized fixture/E2E corpus and make its deterministic reliability checks part of prompt/model promotion.
2. Benchmark the current three-call strategy against a single structured call before changing orchestration.
3. Add retry jitter, `Retry-After`, and retry telemetry within the existing overall deadline.
4. Add scheduled model availability/deprecation checks and logical model profiles if exact model-ID operations become burdensome.
5. Automate the documented version/checksum/release controls; add signatures if required by the supply-chain policy.
6. Add opt-in structured `ai_analysis` output after downstream schema compatibility is proven.
7. Remove or implement reserved config fields through a documented migration when their disposition is decided.

### Only when justified by measurements

1. Parallel map/reduce analysis for large logs.
2. A broader provider-neutral domain layer and multiple model/provider fallback.
3. A shared or asynchronous enrichment service.
4. Additional PR/CD prompt packs or retrieval of reviewed runbooks.

## Final Recommendation

Proceed with the proposal and recognize the current repository as a complete MVP, not just an architecture sketch. Keep the CLI as the durable compatibility boundary. The three-call Watson flow is a valid current strategy; treat it as replaceable only after an alternative proves equal or better on the existing safety and quality gates.

The future-proof design is:

- exact fail-safe pass-through at the pipeline boundary;
- explicit versioned input/output contracts;
- conservative eligibility and privacy policy;
- deterministic evidence preparation;
- runtime-validated structured diagnosis, using whichever evaluated call strategy meets quality and operational targets;
- strict schema and evidence validation;
- the existing chat seam, expanded into a provider-neutral core only when runtime schemas or another provider justify it;
- exact runtime model selection today, with logical profiles and lifecycle monitoring when operationally needed;
- measurable quality, latency, cost, and fallback behavior;
- optional map/reduce or service deployment only when operational data demonstrates the need.

This approach preserves the implementation's strongest qualities—safe incremental adoption, exact fallback, strict boundaries, and good testability—while improving runtime output assurance, operational visibility, governance, and future migration options without discarding work that is already complete.
