# Watson AI Status Wrapper Architecture

## Goal

Build an independent Go-based AI wrapper that can be inserted into the cloud onboarding repository with minimal Tekton pipeline changes.

The wrapper receives the JSON status produced by the existing capture-error flow, determines whether the command succeeded or failed, and returns a JSON status document. For successful commands, it must return the original JSON unchanged. For failed commands, it should call Watson AI to analyze `stdout` and `stderr`, then update the original JSON `error_message` field with a developer-focused diagnosis and suggested fix.

The wrapper must be fail-safe. If the AI wrapper encounters any internal issue, such as a configuration error, token error, API timeout, invalid AI response, or network failure, it must return the original status JSON unchanged to preserve the existing pipeline behavior.

## Developer Skills

A developer does not need to be an expert in every area before working on this repository. The following skills are the minimum needed to start safely:

- Basic Go knowledge: packages, structs, interfaces, error handling, JSON, unit tests, and the `context` and `net/http` packages.
- Basic CI/CD knowledge: shell commands, environment variables, exit codes, standard input/output, and how a pipeline passes status between steps.
- Basic GenAI knowledge: prompts, model input/output, token and context limits, hallucination risk, and why model responses must be treated as untrusted output.
- Basic API and security knowledge: HTTP requests, timeouts, retries, bearer tokens, secret handling, log redaction, and avoiding credentials in source code or logs.
- Ability to read configuration and tests: YAML, prompt templates, test fixtures, and existing Go tests should be reviewed before changing behavior.

Developers can learn the deeper topics while working on maintenance tasks. Over time, they should become comfortable with Watsonx APIs and IAM, Tekton concepts, prompt evaluation, large-log reduction, structured logging, secure CI/CD design, and the wrapper's fail-safe behavior. Changes to authentication, status classification, fallback behavior, prompt security, or the `stdout` JSON contract require additional care and review because mistakes in these areas can affect pipeline reliability or expose sensitive data.

## Current Flow

Existing command pattern:

```bash
status="$(./scripts/capture-error/capture-error.sh \
  --exit-code-only \
  --redaction-regex-file /tmp/capture-redaction-patterns.txt \
  -- ./scripts/capture-error/capture-error-scenarios.sh --any-execution-script/command)"
```

The current output is a JSON document such as:

```json
{
  "success": false,
  "status": "failed",
  "exit_code": 127,
  "wrapper_exit_code": 127,
  "error_message": "Command failed with exit code 127.",
  "output": {
    "stdout": "some stdout msg...",
    "stderr": "exit status 1\nexit status 1\n"
  }
}
```

Proposed post-processing pattern:

```bash
raw_status="$(./scripts/capture-error/capture-error.sh \
  --exit-code-only \
  --redaction-regex-file /tmp/capture-redaction-patterns.txt \
  -- ./scripts/capture-error/capture-error-scenarios.sh --any-execution-script/command)"

status="$(printf '%s' "$raw_status" | ./bin/ai-status-wrapper \
  --config ./config/ai-status-wrapper/config.yaml \
  --prompts ./config/ai-status-wrapper/prompts \
  --pipeline sync \
  --prompt-version v1)"
```

The wrapper reads JSON from `stdin` and writes JSON to `stdout`.

## Success and Failure Decision

Treat the status JSON as successful only when all four fields match:

```json
{
  "success": true,
  "status": "success",
  "exit_code": 0,
  "wrapper_exit_code": 0
}
```

Go rule:

```go
func IsSuccessful(s Status) bool {
    return s.Success &&
        s.Status == "success" &&
        s.ExitCode == 0 &&
        s.WrapperExitCode == 0
}
```

Behavior:

| Case | Wrapper action | Output |
| --- | --- | --- |
| Success JSON | Do not call Watson AI | Original JSON unchanged |
| Failure JSON | Analyze `stderr`, analyze `stdout`, ask for final conclusion | Original JSON with improved `error_message` |
| Wrapper internal failure | Do not change pipeline result | Original JSON unchanged |
| JSON parse failure | Wrapper cannot safely enrich | Return original input bytes unchanged |

The wrapper process should exit `0` whenever it successfully emits a JSON document or original input. This keeps the wrapper as a post-processor and prevents AI failure from changing Tekton behavior. The command status remains represented by `exit_code` and `wrapper_exit_code` inside the JSON.

## High-Level Architecture

```text
Tekton task
  |
  | capture-error.sh returns status JSON
  v
ai-status-wrapper CLI
  |
  | parse status JSON
  | check success fields
  |
  +-- success ----------------------------+
  |                                       |
  | return original JSON unchanged         |
  |                                       |
  +-- failure ----------------------------+
      |
      | load config and prompt files
      | get IAM bearer token
      |
      +--> Watson call 1: stderr analysis
      |
      +--> Watson call 2: stdout analysis
      |
      +--> Watson call 3: final developer suggestion
      |
      | update status.error_message
      v
  final status JSON to stdout
```

## Recommended Repository Layout

Use an independent package so it can be moved into the cloud onboarding repository without coupling to the existing capture-error implementation.

```text
scripts/
  ai-status-wrapper/
    ai-status-wrapper.sh              # Optional shell entrypoint used by Tekton

cmd/
  ai-status-wrapper/
    main.go                           # CLI: flags, stdin/stdout, exit behavior

internal/
  aistatus/
    status.go                         # Status JSON structs and success detection
    wrapper.go                        # Main orchestration logic
    wrapper_test.go

  watsonx/
    client.go                         # Watson chat API client
    iam.go                            # IBM IAM token client and token cache
    model.go                          # Model selection from config
    client_test.go
    iam_test.go

  prompts/
    loader.go                         # Loads system/user/assistant prompt files
    renderer.go                       # Injects stdout/stderr/status context
    loader_test.go

  config/
    config.go                         # YAML config loader and validation
    config_test.go

  logprep/
    sanitize.go                       # Optional extra redaction before AI calls
    chunk.go                          # Token/size-aware log truncation/chunking
    sanitize_test.go
    chunk_test.go

config/
  ai-status-wrapper/
    config.yaml
    prompts/
      common/
      sync/v1/
      pr/v1/
      cd/v1/

testdata/
  status/
    success.json                      # Unit/integration test fixture
    failure.json                      # Unit/integration test fixture
```

## CLI Contract

Recommended command:

```bash
./bin/ai-status-wrapper \
  --config ./config/ai-status-wrapper/config.yaml \
  --prompts ./config/ai-status-wrapper/prompts \
  --pipeline sync \
  --prompt-version v1 \
  < status.json
```

Optional flags:

| Flag | Purpose |
| --- | --- |
| `--config` | Path to YAML config |
| `--prompts` | Directory containing prompt templates |
| `--input` | Optional file input instead of `stdin` |
| `--output` | Optional file output instead of `stdout` |
| `--pipeline` | Pipeline prompt pack to use, for example `sync`, `pr`, or `cd` |
| `--prompt-version` | Prompt pack version, for example `v1` |
| `--timeout` | Overall wrapper timeout |
| `--dry-run` | Parse and classify JSON without calling Watson |
| `--log-level` | Logging level: `off`, `error`, `info`, or `debug` |
| `--debug` | Compatibility shortcut that overrides the log level to `debug` |

Important output rule:

`stdout` must contain only the final JSON. Logs and wrapper diagnostics must go to `stderr`, otherwise the pipeline variable will contain invalid JSON.

## Configuration Design

Keep credentials out of YAML. Store the IBM API key in Tekton secret/env var:

```bash
export WATSONX_API_KEY="..."
```

Recommended config:

```yaml
watsonx:
  url: "https://us-south.ml.cloud.ibm.com"
  api_version: "2024-05-31"
  project_id: "<watsonx-project-id>"
  iam_token_url: "https://iam.cloud.ibm.com/identity/token"

model_selection:
  selected: 0
  models:
    - id: "openai/gpt-oss-120b"
      name: "OpenAI GPT-OSS 120B"
      context_limit_tokens: 131072
    - id: "meta-llama/llama-3-3-70b-instruct"
      name: "Meta Llama 3.3 70B Instruct"
      context_limit_tokens: 131072

prompting:
  pipeline: "sync"
  version: "v1"
  allow_common_fallback: false
  enable_few_shot: true
  max_examples_per_call: 2
  metrics_label: "sync-v1"

generation:
  default_max_output_tokens: 4096
  fresh_max_input_tokens: 24000
  fresh_max_output_tokens: 4096
  final_max_total_input_tokens: 64000
  final_max_output_tokens: 1024
  time_limit_ms: 10000

http:
  timeout_seconds: 30
  retry_count: 2
  retry_backoff_ms: 500
  body_warning_bytes: 524288
  body_hard_limit_bytes: 1048576

chunking:
  chunk_size_tokens: 1024
  chunk_overlap_tokens: 128

fallback:
  return_original_on_ai_error: true
  return_original_on_config_error: true
```

The `selected` model index satisfies the requirement:

| Value | Model |
| --- | --- |
| `0` | `openai/gpt-oss-120b` |
| `1` | `meta-llama/llama-3-3-70b-instruct` |

This structure can be extended by appending more models to the `models` list.

## Prompt File Design

Use one common prompt-loading engine, but keep separate prompt sets for each pipeline scenario. Sync jobs, PR validation, and CD deployments can exhibit different failure modes, and using one generic prompt for all of them will make the AI result less precise and harder to tune.

Recommended approach:

- Keep pipeline-specific prompts for `sync`, `pr`, and `cd`.
- Keep separate prompts for each call type: `stderr` fresh call, `stdout` fresh call, and final context call.
- Keep separate `system`, `user`, and optional `assistant` files for each call.
- Add prompt versions from the beginning so performance can be compared across prompt changes.
- Use `common/` prompts only as fallback or shared fragments, not as the main production prompt for every pipeline.

Recommended prompt files:

```text
config/ai-status-wrapper/prompts/
  common/
    fragments/
      response-schema.md
      safety-rules.md
    examples/
      generic-go-build-failure.md

  sync/
    v1/
      stderr/
        fresh.system.md
        fresh.user.md
        fresh.assistant.md
      stdout/
        fresh.system.md
        fresh.user.md
        fresh.assistant.md
      final/
        context.system.md
        context.user.md
        context.assistant.md
      examples/
        profile-diff-failure.md

  pr/
    v1/
      stderr/
        fresh.system.md
        fresh.user.md
        fresh.assistant.md
      stdout/
        fresh.system.md
        fresh.user.md
        fresh.assistant.md
      final/
        context.system.md
        context.user.md
        context.assistant.md
      examples/
        unit-test-failure.md
        lint-failure.md

  cd/
    v1/
      stderr/
        fresh.system.md
        fresh.user.md
        fresh.assistant.md
      stdout/
        fresh.system.md
        fresh.user.md
        fresh.assistant.md
      final/
        context.system.md
        context.user.md
        context.assistant.md
      examples/
        deploy-timeout.md
        permission-denied.md
```

The `assistant` files should be optional. Use them for the expected answer structure, examples, or few-shot responses. If no useful example is available, the wrapper can send only `system` and `user` messages.

Prompt resolution should be deterministic:

1. Load `prompts/<pipeline>/<version>/<target>/<call>.<role>.md`, where `target` is `stderr`, `stdout`, or `final`.
2. If optional `assistant` prompt is missing, continue without it.
3. If a required `system` or `user` prompt is missing, return the original JSON unchanged.
4. Do not silently switch from `sync` to `common` in production unless config explicitly allows fallback.

This lets the same binary support all pipelines:

```bash
./bin/ai-status-wrapper --pipeline sync --prompt-version v1
./bin/ai-status-wrapper --pipeline pr --prompt-version v1
./bin/ai-status-wrapper --pipeline cd --prompt-version v1
```

### Example stderr Fresh Prompt

`sync/v1/stderr/fresh.system.md`:

```text
You are a CI/CD failure analysis assistant. Analyze stderr from a Tekton pipeline command.
Return concise JSON with errors, warnings, likely root cause, and missing context.
Do not invent facts that are not supported by the log.
```

`sync/v1/stderr/fresh.user.md`:

```text
Command:
{{command}}

Exit code:
{{exit_code}}

stderr:
{{stderr}}
```

`sync/v1/stdout/fresh.system.md`:

```text
You are a CI/CD log analysis assistant. Analyze stdout from a Tekton pipeline command.
Find warnings, suspicious messages, dependency/version problems, and useful context.
Return concise JSON.
```

`sync/v1/stdout/fresh.user.md`:

```text
Command:
{{command}}

Exit code:
{{exit_code}}

stdout:
{{stdout}}
```

`sync/v1/final/context.system.md`:

```text
You are a senior cloud onboarding engineer helping developers fix Tekton pipeline failures.
Use the stderr analysis and stdout analysis to produce a final diagnosis and fix plan.
Use only explicit log/status evidence; an echoed command is not evidence that its executable is missing.
Account for Tekton step-container isolation. Cross-step files require a shared volume or workspace.
For Mike Farah yq v4, avoid an unqualified distro package and require the correct OS/architecture plus integrity verification.
Keep the complete response at or below 180 words.
```

`sync/v1/final/context.user.md`:

```text
Original status JSON summary:
{{status_summary}}

stderr analysis:
{{stderr_analysis}}

stdout analysis:
{{stdout_analysis}}

Return a concise developer-facing message with:
1. Main issue
2. Evidence from logs
3. Most likely root cause
4. Recommended fix
5. Follow-up checks

Use only evidence shown above. Do not infer that a tool is missing merely because its command appears in stdout.
```

`sync/v1/final/context.assistant.md`:

```text
Main issue: <single most important failure>
Evidence: <specific log evidence from stderr/stdout analysis>
Most likely root cause: <practical root cause>
Recommended fix: <actionable fix>
Follow-up checks: <short validation checklist>
```

### Few-Shot Examples

Few-shot examples should be added per pipeline when recurring known failures are identified. Keep them concise and specific.

Suitable candidates:

- Sync pipeline: profile diff failures, missing generated files, dependency download failures, config mismatch.
- PR pipeline: unit test failures, lint failures, coverage failures, invalid YAML, merge-base problems.
- CD pipeline: deployment timeout, permission denied, missing secret, image pull failure, rollout failure.

Do not include every historical failure in the prompt. Select high-value examples that represent common patterns. Too many examples increase token cost and can distract the model from the current logs.

## Watson API Flow

### 1. IAM Token

The wrapper gets a bearer token from IBM IAM:

```bash
curl --location 'https://iam.cloud.ibm.com/identity/token' \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'grant_type=urn:ibm:params:oauth:grant-type:apikey' \
  --data-urlencode 'apikey=<API-KEY>'
```

Implementation notes:

- Read API key from `WATSONX_API_KEY`.
- Cache token in memory for a single wrapper execution.
- If token generation fails, return original JSON unchanged.
- Never write token or API key to logs.

### 2. Fresh stderr Call

Use only stderr-specific prompt context and `output.stderr`.

Purpose:

- Identify explicit errors.
- Identify warnings in stderr.
- Extract command failure signals.
- Produce structured analysis for the final call.

### 3. Fresh stdout Call

Use only stdout-specific prompt context and `output.stdout`.

Purpose:

- Identify warnings or hidden failure context in stdout.
- Detect dependency, environment, version, profile, or command output clues.
- Produce structured analysis for the final call.

### 4. Final Context Call

Use:

- Original status summary.
- Result of stderr call.
- Result of stdout call.
- Command display and args.
- Exit code and failure reason.

Purpose:

- Create one final developer-facing diagnosis.
- Explain the main reason behind the failure.
- Suggest the most practical fix.

The final response becomes the new `error_message` value.

## Watson Chat Request Shape

Recommended request structure:

```json
{
  "messages": [
    {
      "role": "system",
      "content": "system prompt text"
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "rendered user prompt text"
        }
      ]
    }
  ],
  "parameters": {
    "max_new_tokens": 4096,
    "time_limit": 10000
  },
  "model_id": "openai/gpt-oss-120b",
  "project_id": "<watsonx-project-id>"
}
```

When `enable_few_shot` is true, the wrapper can insert rendered example and assistant messages before the final user message. Keep these examples small and pipeline-specific.

Endpoint:

```text
POST https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2024-05-31
```

## Status JSON Mutation Rules

Keep mutation minimal.

For success:

- Return exact original JSON.
- No formatting changes if possible.
- No Watson calls.

For failure with successful AI analysis:

- Preserve all existing fields.
- Update only `error_message`.
- Keep `success`, `status`, `exit_code`, and `wrapper_exit_code` unchanged.

Example final `error_message` format:

```text
AI analysis: The command failed with exit code 127. Main issue: the script or command was not found or could not be executed. Evidence: stderr repeats "exit status 1" and the status failure_reason is "non_zero_exit_code". Recommended fix: verify ./scripts/travis/profile_diff.sh exists in the Tekton workspace, has executable permission, and all required runtime dependencies are installed before this step runs. Follow-up checks: confirm the working directory, PATH, script shebang, and mounted repository contents.
```

Optional future enhancement:

```json
{
  "ai_analysis": {
    "enabled": true,
    "model_id": "openai/gpt-oss-120b",
    "stderr_summary": "...",
    "stdout_summary": "...",
    "final_summary": "..."
  }
}
```

Keep this optional because downstream Tekton consumers may expect the current schema.

## Error Handling and Fallback

The wrapper should use a single fallback rule:

```text
If enrichment cannot complete safely, return the original status JSON unchanged.
```

Fallback cases:

- Cannot read config.
- Invalid model selection.
- Missing `WATSONX_API_KEY`.
- IAM token request fails.
- Watson chat request fails.
- Watson response cannot be parsed.
- Prompt file missing.
- Input JSON missing expected fields.
- Context/body size exceeds hard limit.
- Overall wrapper timeout is reached.

Diagnostics should be written to `stderr` only:

```text
ai-status-wrapper: Watson enrichment failed: IAM token request returned 401; returning original JSON
```

Never write diagnostics to `stdout`.

### Logging

Use Go's standard `log/slog` package for structured runtime diagnostics and write all logs to `stderr`. The default level is `error`; it can be set with `AI_STATUS_WRAPPER_LOG_LEVEL` or `--log-level`, with the CLI flag taking precedence. `--debug` overrides both and selects `debug`. Logging may be disabled with `--log-level off` without changing wrapper behavior.

## Log Size and Context Management

The sample success JSON shows large stdout with truncation:

```json
{
  "stdout_raw_bytes": 10948909,
  "stdout_truncated": true,
  "output_truncated": true
}
```

The wrapper should not send full logs to Watson without first applying size controls.

Recommended log preparation:

1. Prefer existing captured `output.stdout` and `output.stderr`.
2. Apply redaction again as defense in depth if patterns are available.
3. If content is too large, keep:
   - first N lines,
   - last N lines,
   - lines containing error/warn/fail/exception/panic/timeout/denied/not found,
   - command and summary metadata.
4. Include truncation notice in prompt:

```text
Note: stdout was truncated by capture-error. Analyze only the available log content.
```

## Security Requirements

- Store Watson API key in Tekton secret, not in Git.
- Do not include secrets in `config.yaml`.
- Reuse existing `capture-error` redaction patterns where possible.
- Add wrapper-side redaction before external API calls.
- Never log request bodies by default.
- Never log IAM bearer token.
- Keep debug mode disabled in CI by default.

## Suggested Go Types

```go
type Status struct {
    Success         bool            `json:"success"`
    Status          string          `json:"status"`
    ExitCode        int             `json:"exit_code"`
    WrapperExitCode int             `json:"wrapper_exit_code"`
    FailureReason   *string         `json:"failure_reason"`
    ErrorMessage    *string         `json:"error_message"`
    Command         Command         `json:"command"`
    Summary         Summary         `json:"summary"`
    Output          Output          `json:"output"`
    Raw             json.RawMessage `json:"-"`
}

type Output struct {
    Stdout string `json:"stdout"`
    Stderr string `json:"stderr"`
}
```

For preserving unknown fields, use either:

- a typed struct plus `map[string]any` merge, or
- decode into `map[string]any` for mutation and use helper functions for known fields.

The second option is safer if existing pipeline JSON may add fields later.

## Development Plan

1. Add config loader and validation.
2. Add status parser and success/failure classifier.
3. Add prompt loader and renderer.
4. Add IBM IAM token client.
5. Add Watson chat client.
6. Add wrapper orchestration:
   - parse input,
   - pass through success,
   - enrich failure,
   - fallback to original on any error.
7. Add shell entrypoint for Tekton.
8. Add unit tests with fake HTTP server.
9. Add integration test that runs the CLI against `testdata/status/success.json` and `testdata/status/failure.json`.

## Test Strategy

Unit tests:

| Test | Expected result |
| --- | --- |
| Success JSON classification | No Watson call, original JSON returned |
| Failure JSON classification | Three Watson calls are made |
| IAM token failure | Original JSON returned |
| Watson stderr call failure | Original JSON returned |
| Watson stdout call failure | Original JSON returned |
| Watson final call failure | Original JSON returned |
| Missing API key | Original JSON returned |
| Invalid config | Original JSON returned |
| Invalid JSON input | Original input returned |
| Large stdout/stderr | Logs are reduced before request |
| Model selected `0` | Uses `openai/gpt-oss-120b` |
| Model selected `1` | Uses `meta-llama/llama-3-3-70b-instruct` |
| Pipeline prompt selection | Uses the expected `prompts/<pipeline>/<version>/` files |
| Required prompt missing | Original JSON returned |

CLI tests:

```bash
go test ./...

go run ./cmd/ai-status-wrapper \
  --config ./config/ai-status-wrapper/config.yaml \
  --prompts ./config/ai-status-wrapper/prompts \
  --pipeline sync \
  --prompt-version v1 \
  < ./testdata/status/success.json

go run ./cmd/ai-status-wrapper \
  --config ./config/ai-status-wrapper/config.yaml \
  --prompts ./config/ai-status-wrapper/prompts \
  --pipeline sync \
  --prompt-version v1 \
  < ./testdata/status/failure.json
```

For CI, mock Watson APIs by using `httptest.Server`. Do not call real Watson endpoints in normal unit tests.

### Real End-to-End Test Proposal

Provide an opt-in test that runs the real CLI flow against IBM IAM and Watsonx using the synthetic JSON fixtures in `testdata/status`. Keep it disabled during normal test runs to avoid requiring credentials, network access, model quota, or cost.

```bash
export WATSONX_API_KEY="..."
export WATSONX_PROJECT_ID="..."
export WATSONX_MODEL_ID="openai/gpt-oss-120b"
export RUN_WATSONX_E2E=1

go test ./cmd/ai-status-wrapper \
  -run '^TestRealWatsonEndToEndScore$' \
  -count=1 -v
```

The default run should discover every JSON fixture. A success fixture must be returned byte-for-byte without a Watson call. Each failure fixture must complete the IAM exchange and three Watson calls, then satisfy all of the following acceptance criteria:

- The wrapper exits `0` and preserves every status field except `error_message`.
- The new message starts with `AI analysis:` and uses evidence from the captured command or logs.
- The diagnosis includes actionable remediation and passes fixture-specific reliability checks.
- The response contains no known misleading guidance, stays within 180 words, and reaches the default quality score of at least `70/100`.

Field preservation and reliability are mandatory even when the total score reaches the configured threshold. Allow `WATSONX_E2E_FIXTURE` to select one fixture for debugging and `WATSONX_E2E_MIN_SCORE` to raise the quality threshold when evaluating a model or prompt change. Because model output can vary, investigate repeated failures by reviewing the score breakdown and generated message before changing prompts, models, or acceptance rules.

## Tekton Integration

Recommended minimal Tekton script change:

```bash
raw_status="$(./scripts/capture-error/capture-error.sh \
  --exit-code-only \
  --redaction-regex-file /tmp/capture-redaction-patterns.txt \
  -- ./scripts/capture-error/capture-error-scenarios.sh --any-execution-script/command)"

status="$(printf '%s' "$raw_status" | ./bin/ai-status-wrapper \
  --config ./config/ai-status-wrapper/config.yaml \
  --prompts ./config/ai-status-wrapper/prompts \
  --pipeline sync \
  --prompt-version v1)"

printf '%s\n' "$status"
```

Tekton secret example:

```yaml
env:
  - name: WATSONX_API_KEY
    valueFrom:
      secretKeyRef:
        name: watsonx-ai-secret
        key: api-key
```

## Operational Defaults

Recommended production defaults:

- AI enrichment enabled only for failure JSON.
- Wrapper timeout should be short, for example 30 to 60 seconds total.
- Retry Watson calls only for transient `429` and `5xx` responses.
- Do not retry `400`, `401`, `403`, or invalid request errors.
- Return original JSON if final AI message is empty.
- Keep final `error_message` concise enough for pipeline logs.

## Extension for PR and CD Pipelines

PR and CD should be supported by prompt packs, not by changing the wrapper logic. The first implementation can ship with only the `sync/v1` prompt pack, but the directory structure and CLI/config should already support `--pipeline pr` and `--pipeline cd`.

When a new pipeline is added:

1. Add a new prompt pack under `prompts/<pipeline>/<version>/`.
2. Add pipeline-specific few-shot examples for known failures.
3. Add tests proving the wrapper selects the expected prompt files.
4. Track the prompt version in logs or metrics, for example `sync-v1`, `pr-v1`, or `cd-v1`.

The core Go package should stay unchanged. Only prompt files, prompt examples, and pipeline metadata should change.

## Recommended First Milestone

For the first implementation, keep the scope small:

1. CLI reads status JSON from `stdin`.
2. Success status returns unchanged.
3. Failure status performs three Watson calls.
4. Final call output replaces `error_message`.
5. Prompt selection supports `pipeline` and `prompt-version`, with `sync/v1` implemented first.
6. Any wrapper error returns original JSON unchanged.
7. Tests use fake Watson and IAM servers.

This establishes a safe, maintainable wrapper that can be inserted into the current sync job pipeline first, then expanded to PR and CD pipelines later.
