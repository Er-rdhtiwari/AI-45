# AI Status Wrapper

`ai-status-wrapper` is an independent Go command that enriches failed CI/CD status JSON with a developer-focused Watson AI diagnosis. It is designed to run after an existing command-status collector, such as `capture-error.sh`, without changing the collector or the downstream JSON contract.

The wrapper reads one status document of up to 10 MiB from standard input or a file and writes one status document to standard output or a file.

- A successful status is returned byte-for-byte without calling Watson.
- A failed status triggers separate `stderr` and `stdout` Watson calls, followed by a final synthesis call.
- Successful enrichment changes only the `error_message` value.
- Any wrapper failure returns the exact original input and exits successfully after writing it.
- Diagnostics are written only to `stderr`; `stdout` is reserved for the status document.

The module requires Go 1.23 or newer and uses only the Go standard library. It has no third-party Go dependencies.

## Contents

- [Core guarantees](#core-guarantees)
- [Processing flow](#processing-flow)
- [Input and output contract](#input-and-output-contract)
- [Repository structure](#repository-structure)
- [Packages and modules](#packages-and-modules)
- [Configuration reference](#configuration-reference)
- [Build and run](#build-and-run)
- [Logging](#logging)
- [Integrate into another repository](#integrate-into-another-repository)
- [Tekton integration](#tekton-integration)
- [Prompt development](#prompt-development)
- [Security](#security)
- [Failure, timeout, and retry behavior](#failure-timeout-and-retry-behavior)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Developer maintenance guide](#developer-maintenance-guide)
- [Current limitations and future work](#current-limitations-and-future-work)

## Core guarantees

The wrapper is a post-processor, not the authority that decides whether the pipeline command should fail. The original command result remains represented by `success`, `status`, `exit_code`, and `wrapper_exit_code` inside the JSON.

| Situation | Behavior | Process exit code |
| --- | --- | --- |
| Valid successful status | Return the exact original bytes; make no IAM or Watson call | `0` |
| Valid failed status and AI succeeds | Preserve all fields and replace `error_message` | `0` |
| Invalid input JSON | Return the exact original bytes | `0` |
| Missing required status field | Return the exact original bytes | `0` |
| Invalid config or prompt | Return the exact original bytes | `0` |
| Missing API key or IAM failure | Return the exact original bytes | `0` |
| Watson HTTP, timeout, size, or response failure | Return the exact original bytes | `0` |
| Cannot read the requested input | No safe document can be emitted | `1` |
| Cannot write the requested output | Output delivery failed | `1` |
| Invalid CLI arguments | Print usage error to `stderr` | `2` |

This behavior is intentionally fail-safe. Do not change fallback errors into nonzero process exits without first reviewing every Tekton consumer, because doing so can cause an optional AI enhancement to disrupt an otherwise functioning pipeline.

## Processing flow

```text
capture-error status JSON
          |
          v
  cmd/ai-status-wrapper
          |
          v
  aistatus.Parse
          |
          +-- invalid --------------------------> exact original input
          |
          +-- exact success --------------------> exact original input
          |
          +-- failure
                 |
                 +--> load and validate config
                 +--> load prompt pack
                 +--> redact/reduce stderr
                 +--> IAM token --> Watson call 1: stderr analysis
                 +--> redact/reduce stdout
                 +--> cached token --> Watson call 2: stdout analysis
                 +--> both analyses + status --> Watson call 3: final diagnosis
                 |
                 +-- any error ----------------> exact original input
                 |
                 +-- success --> replace error_message --> enriched JSON
```

The three Watson requests are independent HTTP requests. The two fresh analysis requests do not share model conversation history. Only the third request receives the results of both earlier analyses.

## Input and output contract

### Required classification fields

The input must be a top-level JSON object containing these fields with the shown types:

```json
{
  "success": false,
  "status": "failed",
  "exit_code": 127,
  "wrapper_exit_code": 127
}
```

A document is successful only when all four conditions are true:

```text
success == true
status == "success"
exit_code == 0
wrapper_exit_code == 0
```

Every other valid combination is classified as failure.

### Additional failure fields

A failed status must contain string-valued `stdout` and `stderr` fields:

```json
{
  "output": {
    "stdout": "command output",
    "stderr": "command error output"
  }
}
```

`command`, `summary`, `failure_reason`, and the original `error_message` are used when available but are not required for classification.

### Output behavior

For success and every fallback case, output is byte-for-byte identical to input. This includes whitespace, key order, and trailing newline behavior.

For successful failure enrichment:

- Unknown fields and nested values are preserved.
- Only the semantic value of `error_message` changes.
- The output is re-encoded as indented JSON, so whitespace and object-key order may differ from the input.
- The final message is prefixed with `AI analysis:` unless the model already supplied that prefix.

Example:

```json
{
  "success": false,
  "status": "failed",
  "exit_code": 127,
  "wrapper_exit_code": 127,
  "error_message": "AI analysis: Main issue: the command is unavailable. Evidence: stderr reports command not found. Recommended fix: install the command or correct the executable path."
}
```

### Standard streams

Treat the two output streams as separate API contracts:

- `stdout`: only the final or fallback status content.
- `stderr`: structured `log/slog` diagnostics, CLI usage errors, and debug messages.

Never redirect `stderr` into `stdout` when assigning the result to a shell variable.

## Repository structure

```text
ai-wrapper/
  go.mod
  Makefile
  README.md
  watson-ai-wrapper-architecture.md

  cmd/
    ai-status-wrapper/
      main.go
      main_test.go
      real_e2e_test.go

  internal/
    aistatus/
      status.go
      wrapper.go
      status_test.go
      wrapper_test.go
    config/
      config.go
      yaml.go
      config_test.go
      yaml_test.go
    logprep/
      sanitize.go
      chunk.go
      logprep_test.go
    prompts/
      loader.go
      renderer.go
      loader_test.go
    watsonx/
      iam.go
      client.go
      iam_test.go
      client_test.go

  config/
    ai-status-wrapper/
      config.yaml
      prompts/
        sync/v1/...

  scripts/
    ai-status-wrapper/
      ai-status-wrapper.sh

  testdata/
    status/
      success.json
      failure.json
      failure-permission-denied.json
      failure-rollout-timeout.json
      failure-invalid-kubernetes-yaml.json
```

## Packages and modules

### Go module: `ai-status-wrapper`

File: `go.mod`

This is a standalone Go module so the complete `ai-wrapper` directory can be copied into another repository without depending on that repository's Go module. It declares Go 1.23 and contains no `require` entries.

Keeping it as a nested standalone module provides several benefits:

- Parent-repository dependencies cannot affect wrapper builds.
- The wrapper does not add dependencies to the parent `go.mod`.
- Parent `go test ./...` normally does not enter the nested module.
- The wrapper can be tested and built independently with `go -C ai-wrapper ...`.
- It can be packaged as a binary or container without exposing Go APIs to the host repository.

### Command package: `cmd/ai-status-wrapper`

Files: `main.go`, `main_test.go`, `real_e2e_test.go`

This package owns the process boundary and should remain thin. It is responsible for:

- Defining and parsing CLI flags.
- Reading standard input or `--input`.
- Classifying input before loading Watson configuration.
- Returning successful input without touching config, prompts, credentials, or the network.
- Creating the HTTP client, IAM client, Watson client, sanitizer, prompt loader, and processor.
- Creating the standard-library `log/slog` logger and applying log-level filtering.
- Applying the overall context timeout.
- Writing the enriched or fallback result to standard output or `--output`.
- Keeping diagnostics off standard output.
- Mapping only CLI and operating-system I/O failures to nonzero exits.

`main_test.go` exercises the command as an integrated unit with local fake IAM and Watson HTTP servers. It verifies the one-IAM/three-Watson request flow and exact pass-through behavior.

`real_e2e_test.go` discovers the status fixtures and contains the opt-in live Watson scoring test. It runs all fixtures by default or one fixture selected with `WATSONX_E2E_FIXTURE`.

When adding a CLI flag, update all of the following:

1. `main.go` flag declaration and wiring.
2. The CLI flag table in this README.
3. Tests for its normal and fallback behavior.
4. Tekton examples if pipeline invocation changes.

### Status package: `internal/aistatus`

Files: `status.go`, `wrapper.go`, and their tests.

This is the core orchestration package.

`status.go` contains:

- `Document`: an internal representation of the parsed status plus the untouched original bytes.
- `Parse`: strict JSON parsing with required-field and type validation.
- `Document.IsSuccessful`: the four-field success rule.
- Accessors for logs, command display, exit code, and truncation metadata.
- `SummaryJSON`: a bounded selection of status context for the final model call.
- `WithErrorMessage`: mutation and re-encoding after successful enrichment.

`wrapper.go` contains:

- `Processor`: dependencies required for enrichment.
- `Processor.Process`: safe library-level processing that always returns original bytes with an error when enrichment cannot complete.
- `Processor.Enrich`: the stderr, stdout, and final-call sequence.
- Prompt value construction and message ordering.
- Redaction and log reduction before external calls.
- Final `AI analysis:` prefixing.

This package depends on `config`, `logprep`, `prompts`, and the small `watsonx.ChatClient` interface. Tests use a fake chat client, so orchestration tests never access a network.

If the capture-error schema changes, begin the update in `status.go`. Preserve `Document.original` and keep unknown-field preservation tests in place.

### Configuration package: `internal/config`

Files: `config.go`, `yaml.go`, and their tests.

`config.go` defines the typed configuration model, default values, validation, and selected-model lookup. Validation covers required values, model index bounds, context limits, HTTP limits, retry bounds, generation limits, and chunk settings.

`yaml.go` is a deliberately small standard-library-only YAML-subset parser. It supports the syntax used by the shipped configuration:

- Indentation-based mappings.
- Indentation-based lists.
- Plain, single-quoted, and double-quoted strings.
- Integers, floating-point values, booleans, and null.
- Full-line and safe inline comments.
- Lists of mappings, such as the model list.

It intentionally rejects:

- Anchors and aliases.
- Tags and merge keys.
- Block scalars.
- Duplicate keys.
- Tabs used for indentation.
- Multi-document YAML.
- Mixed mapping and sequence entries at one indentation level.

Do not replace this parser with a third-party YAML library. If new configuration needs unsupported YAML syntax, prefer expressing it using the current subset or extend the parser with focused tests.

### Log preparation package: `internal/logprep`

Files: `sanitize.go`, `chunk.go`, and `logprep_test.go`.

`sanitize.go` provides defense-in-depth redaction:

- `NewSanitizer` always applies baseline redaction for common labeled credentials and bearer authorization headers.
- `NewSanitizer` compiles regex patterns using Go's standard `regexp` package.
- `PatternsFromFile` reads additional newline-delimited patterns.
- `Sanitizer.Apply` replaces every match with `[REDACTED]`.

Redaction is applied to data sent to Watson. It does not modify fallback output or mutate original captured logs.

`chunk.go` provides `Reduce`, which limits oversized logs using an approximate four-bytes-per-token calculation. It retains:

- The beginning of the log.
- Lines containing failure signals such as error, warning, panic, timeout, denied, or not found.
- The end of the log.
- A notice describing that reduction occurred.

When adding failure signal terms or changing reduction budgets, add tests proving that the important middle and final lines remain present and that the result stays within the byte limit.

### Prompt package: `internal/prompts`

Files: `loader.go`, `renderer.go`, and `loader_test.go`.

`Loader` deterministically resolves a prompt pack from:

```text
<prompt-root>/<pipeline>/<version>/<target>/<call>.<role>.md
```

It requires `system` and `user` files. An `assistant` file is optional. When few-shot prompting is enabled, example Markdown files are loaded alphabetically up to `max_examples_per_call`.

The loader:

- Rejects path traversal in pipeline, version, target, and call segments.
- Rejects prompt and example symlinks that resolve outside the configured prompt root.
- Limits each prompt or example file to 1 MiB.
- Does not silently switch prompt packs.
- Uses `common` fallback only when explicitly enabled.
- Treats a missing required prompt as an enrichment error, causing original-input fallback.

`Render` replaces `{{placeholder}}` values and fails when a template references a value the caller did not provide. This prevents partially rendered prompts from reaching Watson.

Prompt text is runtime data, not compiled into the binary. The prompt directory must therefore be copied or mounted beside the binary and passed with `--prompts`.

### Watson package: `internal/watsonx`

Files: `iam.go`, `client.go`, and their tests.

`iam.go` contains:

- `TokenProvider`: the small interface required by the chat client.
- `IAMClient`: IBM API-key-to-bearer-token exchange.
- Process-local token caching protected by a mutex.
- A 30-second expiration safety margin.
- Retry handling for network failures, HTTP `429`, and HTTP `5xx`.

`client.go` contains:

- Watson chat request and message types.
- Message constructors for system, user, and assistant roles.
- `ChatClient`: the interface consumed by `aistatus.Processor`.
- Watson endpoint construction and authorization.
- Request and response hard-size limits.
- Retry handling for network failures, HTTP `429`, and HTTP `5xx`.
- Parsing for string content, text-block content, and generated-text fallback shapes.

API keys and bearer tokens are never included in returned errors or debug output. Do not add request-body or authorization-header logging.

If IBM changes the Watson response schema, update `parseChatResponse` and add a fixture-driven test before changing orchestration code.

### Runtime configuration and prompt assets

Directory: `config/ai-status-wrapper`

This directory is deployed with the binary and contains:

- `config.yaml`: endpoints, model list, prompt defaults, limits, retries, and redaction patterns.
- `prompts/sync/v1`: the first production prompt pack.
- `prompts/<pipeline>/<version>/examples`: optional few-shot context for known failure patterns.

Configuration and prompts are intentionally separate from code so they can be tuned and versioned without changing the Watson client.

### Shell entrypoint

File: `scripts/ai-status-wrapper/ai-status-wrapper.sh`

This POSIX shell script locates the module root relative to itself and executes `bin/ai-status-wrapper`. It does not build the binary or supply configuration arguments automatically.

Use it when a repository convention prefers scripts over direct binary paths. Pass the same flags you would pass to the binary.

### Fixtures and tests

Directory: `testdata/status`

- `success.json` verifies byte-for-byte success pass-through.
- `failure.json` provides a realistic missing-`yq` profile-diff failure for local and live integration tests.
- `failure-permission-denied.json` models a deployment script without execute permission.
- `failure-rollout-timeout.json` models a Kubernetes deployment that does not finish rolling out.
- `failure-invalid-kubernetes-yaml.json` models a server-side manifest validation failure caused by an invalid field.

Keep fixtures free of credentials, customer data, and very large captured logs.

### Makefile

| Target | Purpose |
| --- | --- |
| `make build` | Build `bin/ai-status-wrapper` |
| `make test` | Run all unit and integration tests |
| `make vet` | Run standard Go static analysis |
| `make fmt` | Format all Go files |
| `make check` | Run tests and vet |
| `make all` | Run checks and build |
| `make clean` | Remove generated binaries |

## Configuration reference

Review `config/ai-status-wrapper/config.yaml` and provide the deployment-specific runtime environment before production use.

### Required setup

1. Inject `WATSONX_PROJECT_ID` through the runtime environment.
2. Optionally set `WATSONX_MODEL_ID` to select a configured model; otherwise the first configured model is used.
3. Inject `WATSONX_API_KEY` through the runtime environment.
4. Confirm the Watson and IAM endpoints are reachable from the pipeline network.

```bash
export WATSONX_API_KEY='...'
export WATSONX_PROJECT_ID='...'
export WATSONX_MODEL_ID='openai/gpt-oss-120b'
```

Never store the API key in YAML, prompts, shell scripts, test fixtures, container build arguments, or source control.

Nonempty `WATSONX_PROJECT_ID` and `WATSONX_MODEL_ID` values override YAML model/project settings before config validation. `WATSONX_MODEL_ID` must exactly match an ID in `model_selection.models`, ensuring the selected model still has a validated context limit.

### Configuration sections

| Section | Active behavior |
| --- | --- |
| `watsonx` | Watson base URL, API version, runtime-overridable project ID, and IAM token endpoint |
| `model_selection` | Model list and optional legacy/default selected index; `WATSONX_MODEL_ID` selects at runtime |
| `prompting` | Default pipeline/version, common fallback, few-shot behavior, and example limit |
| `generation` | Fresh/final input-output budgets and Watson time limit |
| `http` | Client timeout, retries, backoff, and hard request/response size limit |
| `chunking` | Validated settings reserved for future true chunk-by-chunk analysis |
| `security` | Regex patterns applied before sending context to Watson |
| `fallback` | Documents the required fail-safe policy; original-input fallback is currently always enforced |

Some fields are forward-looking:

- `prompting.metrics_label` is available for future metrics integration but is not currently emitted.
- `http.body_warning_bytes` is validated against the hard limit but warning telemetry is not currently emitted.
- `chunking.chunk_size_tokens` and `chunk_overlap_tokens` are validated but current log preparation uses selection-based `Reduce`, not multiple Watson chunk calls.
- `fallback` booleans do not disable fallback; the safety contract is mandatory.

### Model selection

The shipped list is:

| Index | Model ID |
| --- | --- |
| `0` | `openai/gpt-oss-120b` |
| `1` | `meta-llama/llama-3-3-70b-instruct` |

To switch between configured models at runtime, set `WATSONX_MODEL_ID` to an exact model ID. If it is unset, the first model is selected by default. To add a model, append it to `models` with a positive context limit. Config validation ensures the fresh and final input/output budgets fit within the selected model context.

### Redaction patterns

Patterns under `security.redaction_patterns` and patterns read from `--redaction-regex-file` are combined. Each nonempty, non-comment line in the external file is compiled as a Go regular expression.

Example file:

```text
# Internal account IDs
account-[0-9]+

# A repository-specific credential format
MY_TOKEN=[^[:space:]]+
```

An invalid regex causes safe fallback. Test new redaction rules locally because overly broad patterns can remove evidence needed for diagnosis.

## Build and run

### Local development

```bash
make check
make build
```

The binary is written to `bin/ai-status-wrapper` and ignored by Git.

### Run from standard input

```bash
./bin/ai-status-wrapper \
  --config ./config/ai-status-wrapper/config.yaml \
  --prompts ./config/ai-status-wrapper/prompts \
  --pipeline sync \
  --prompt-version v1 \
  < ./testdata/status/failure.json
```

### Run with files

```bash
./bin/ai-status-wrapper \
  --config ./config/ai-status-wrapper/config.yaml \
  --prompts ./config/ai-status-wrapper/prompts \
  --input ./testdata/status/failure.json \
  --output /tmp/enriched-status.json
```

Input is fully read before output is written, so the same file path can be used for both. A separate output path is safer because it retains the original artifact for troubleshooting.

### Classification-only dry run

```bash
./bin/ai-status-wrapper --dry-run < ./testdata/status/failure.json
```

Dry run validates and classifies the document but returns the original bytes. It does not load config or prompts, read the API key, request an IAM token, or call Watson.

### CLI flags

| Flag | Default | Meaning |
| --- | --- | --- |
| `--config` | `./config/ai-status-wrapper/config.yaml` | YAML configuration path |
| `--prompts` | `./config/ai-status-wrapper/prompts` | Prompt-pack root |
| `--input` | standard input | Optional input file |
| `--output` | standard output | Optional output file |
| `--pipeline` | config value | Prompt pipeline override, such as `sync`, `pr`, or `cd` |
| `--prompt-version` | config value | Prompt version override, such as `v1` |
| `--timeout` | `60s` | Overall enrichment deadline covering IAM and all Watson calls |
| `--redaction-regex-file` | none | Additional newline-delimited regex file |
| `--dry-run` | `false` | Classify without loading config or calling Watson |
| `--log-level` | `error` or `AI_STATUS_WRAPPER_LOG_LEVEL` | Select `off`, `error`, `info`, or `debug` |
| `--debug` | `false` | Compatibility shortcut that overrides the level to `debug` |
| `--version` | `false` | Print build version and exit |

Config and prompt paths are resolved from the process working directory, not from the binary location. Always use explicit paths in CI and Tekton.

### Linux build for CI or Tekton

Build for the operating system and architecture used by the pipeline step:

```bash
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
  go build -trimpath -o bin/ai-status-wrapper ./cmd/ai-status-wrapper
```

For ARM64 workers, use `GOARCH=arm64`. Building with `CGO_ENABLED=0` produces a portable static Go binary, but the runtime container still needs CA certificates for HTTPS calls to IBM.

## Logging

All runtime diagnostics use Go's standard `log/slog` package with a text handler. The wrapper does not use the legacy `log` package or `fmt.Printf` for logging. Protocol output, such as the final JSON and `--version`, is written directly and never sent through the logger.

Logs always go to `stderr`. This keeps `stdout` safe for shell command substitution and JSON parsing.

### Log levels

| Level | Behavior |
| --- | --- |
| `off` | Suppress all runtime logs, including fallback and I/O diagnostics |
| `error` | Log fallback, invalid runtime state, and input/output failures; this is the default |
| `info` | Include success pass-through, dry-run, and successful enrichment events |
| `debug` | Include logger initialization, parsed classification, and selected model/prompt configuration |

Each level includes the levels below it in severity. For example, `debug` includes debug, info, and error events; `info` includes info and error events.

Select a level with the CLI:

```bash
./bin/ai-status-wrapper --log-level info < status.json
```

Or set the default through the environment:

```bash
export AI_STATUS_WRAPPER_LOG_LEVEL=error
./bin/ai-status-wrapper < status.json
```

An explicit `--log-level` value overrides the environment default. The existing `--debug` flag is retained for compatibility and overrides both settings to `debug`:

```bash
./bin/ai-status-wrapper --debug < status.json
```

To disable runtime logging completely:

```bash
./bin/ai-status-wrapper --log-level off < status.json
```

CLI flag-parser errors and usage text may still be written to `stderr` because they occur at the command-line boundary before normal runtime processing.

Example text-handler output:

```text
time=2026-07-17T10:00:00.000Z level=ERROR msg="enrichment unavailable; returning original input" component=ai-status-wrapper error="IAM API key is missing"
```

Logging rules for future development:

- Use structured attributes such as `model_id`, `pipeline`, and `prompt_version` instead of formatting values into the message.
- Use `Debug` for developer-only state, `Info` for normal lifecycle events, and `Error` for fallback or failed I/O.
- Never log the API key, bearer token, authorization header, full request body, raw logs, or unredacted status JSON.
- Never use the package-global default logger; pass or create an explicit logger at the process boundary.
- Never point a slog handler at `stdout`.
- Keep error messages useful when logs are enabled, but keep process behavior correct when logging is `off`.

## Integrate into another repository

The recommended integration boundary is the CLI's stdin/stdout contract. The Go implementation lives under `internal/` intentionally and is not designed as a public library imported by unrelated modules.

### Option A: copy as a standalone nested module

This is the recommended source-based approach.

```text
host-repository/
  go.mod                         # optional host module
  scripts/
  pipelines/
  tools/
    ai-wrapper/                  # copy this entire directory
      go.mod
      cmd/
      internal/
      config/
      scripts/
```

Copy the complete directory, preserving prompt and config paths:

```bash
mkdir -p tools
cp -R /path/to/ai-wrapper tools/ai-wrapper
```

Build and test it independently:

```bash
go -C tools/ai-wrapper test ./...
go -C tools/ai-wrapper vet ./...
mkdir -p .tools
(
  cd tools/ai-wrapper
  CGO_ENABLED=0 go build -trimpath \
    -o ../../.tools/ai-status-wrapper ./cmd/ai-status-wrapper
)
```

Invoke it from the host repository root with explicit runtime assets:

```bash
raw_status="$(./scripts/capture-error/capture-error.sh --exit-code-only -- your-command)"

status="$(printf '%s' "$raw_status" | ./.tools/ai-status-wrapper \
  --config ./tools/ai-wrapper/config/ai-status-wrapper/config.yaml \
  --prompts ./tools/ai-wrapper/config/ai-status-wrapper/prompts \
  --pipeline sync \
  --prompt-version v1 \
  --log-level error)"
```

Advantages:

- No modification to the host `go.mod`.
- No third-party downloads.
- Clear ownership and upgrade boundary.
- Independent test and release lifecycle.

To make future upgrades easier, keep repository-specific configuration and prompt packs in clearly identified files or overlay directories. Avoid modifying `internal/` for pipeline-specific wording; prompt changes should normally stay under `config/ai-status-wrapper/prompts`.

Integration checklist:

1. Copy `go.mod`, `cmd`, `internal`, `config`, and tests together.
2. Preserve executable permission on the optional shell entrypoint.
3. Decide whether the host builds the binary or consumes a released artifact.
4. Do not commit a real API key.
5. Inject `WATSONX_PROJECT_ID` and, when needed, `WATSONX_MODEL_ID` for the target environment.
6. Pass explicit config and prompt paths.
7. Make IBM IAM and Watson endpoints available through network policy or proxy configuration.
8. Ensure the runtime image contains trusted CA certificates.
9. Run success and fallback smoke tests before enabling AI enrichment.

### Option B: consume a versioned binary artifact

Build the wrapper once in a trusted release workflow and publish an OS/architecture-specific artifact. The host repository then needs only:

```text
bin/ai-status-wrapper
config/ai-status-wrapper/config.yaml
config/ai-status-wrapper/prompts/...
```

Recommended release controls:

- Embed a version with `make build VERSION=<version>`.
- Publish a SHA-256 checksum.
- Record `GOOS` and `GOARCH` in the artifact name.
- Run tests, race checks, and vet before publishing.
- Distribute config templates without credentials.
- Keep prompt packs versioned with the binary release.

Example:

```bash
make build VERSION=v1.0.0
./bin/ai-status-wrapper --version
shasum -a 256 ./bin/ai-status-wrapper
```

### Option C: package in a container image

A lightweight internal image can contain the Linux binary, CA certificates, config template, and prompt packs. This avoids compiling in each Tekton run.

Keep environment-specific project IDs and API keys outside the image. Mount config through a workspace or ConfigMap and inject the API key through a Secret.

### Importing Go packages directly

Packages below `internal/` can be imported only by code within the parent directory tree, as enforced by Go. An external host module should therefore use the CLI.

If direct library integration becomes a firm requirement, create a reviewed public package such as `pkg/aistatuswrapper` that exposes a small stable API and delegates to internal implementation. Do not simply move all internal types into public packages; that would make configuration, HTTP, and prompt implementation details part of the compatibility contract.

## Tekton integration

### Minimal change inside an existing step

If the binary, config, and prompt pack are already present in the step image or workspace, add one post-processing command:

```bash
raw_status="$(./scripts/capture-error/capture-error.sh \
  --exit-code-only \
  --redaction-regex-file /tmp/capture-redaction-patterns.txt \
  -- ./scripts/capture-error/capture-error-scenarios.sh --all-failure)"

status="$(printf '%s' "$raw_status" | ./bin/ai-status-wrapper \
  --config ./config/ai-status-wrapper/config.yaml \
  --prompts ./config/ai-status-wrapper/prompts \
  --pipeline sync \
  --prompt-version v1 \
  --timeout 45s \
  --log-level error \
  --redaction-regex-file /tmp/capture-redaction-patterns.txt)"

printf '%s\n' "$status"
```

This preserves the existing `status` variable contract. The wrapper's process exit `0` means IAM or Watson failure cannot turn the post-processing command into a Tekton step failure.

### Inject Watson runtime settings

Create the Secret using your organization's secret-management process. A simplified example is:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: watsonx-ai-secret
type: Opaque
stringData:
  api-key: replace-through-secret-management
  project-id: replace-through-secret-management
```

Reference it from the step:

```yaml
env:
  - name: WATSONX_API_KEY
    valueFrom:
      secretKeyRef:
        name: watsonx-ai-secret
        key: api-key
  - name: WATSONX_PROJECT_ID
    valueFrom:
      secretKeyRef:
        name: watsonx-ai-secret
        key: project-id
  - name: WATSONX_MODEL_ID
    value: "openai/gpt-oss-120b"
```

The project ID can instead come from a ConfigMap if it is not considered sensitive in your environment. The model ID is operational configuration and can come from a Tekton parameter or ConfigMap. Do not print the environment, run the shell with `set -x`, or include the API key in Tekton parameters because parameter values may be visible in TaskRun metadata.

### Complete illustrative Tekton Task

This example builds the standard-library-only wrapper in one step and uses it from the shared workspace in the next step. Adapt images, paths, workspaces, and commands to the host repository.

```yaml
apiVersion: tekton.dev/v1
kind: Task
metadata:
  name: run-command-with-ai-status
spec:
  params:
    - name: wrapper-dir
      type: string
      default: tools/ai-wrapper
    - name: pipeline
      type: string
      default: sync
    - name: prompt-version
      type: string
      default: v1
    - name: model-id
      type: string
      default: openai/gpt-oss-120b
  workspaces:
    - name: source
  steps:
    - name: build-ai-status-wrapper
      image: golang:1.23
      workingDir: $(workspaces.source.path)
      script: |
        #!/usr/bin/env sh
        set -eu

        mkdir -p "$(workspaces.source.path)/.tools"
        cd "$(params.wrapper-dir)"
        CGO_ENABLED=0 go build -trimpath \
          -o "$(workspaces.source.path)/.tools/ai-status-wrapper" \
          ./cmd/ai-status-wrapper

    - name: run-and-enrich
      image: your-existing-pipeline-image:tag
      workingDir: $(workspaces.source.path)
      env:
        - name: WATSONX_API_KEY
          valueFrom:
            secretKeyRef:
              name: watsonx-ai-secret
              key: api-key
        - name: WATSONX_PROJECT_ID
          valueFrom:
            secretKeyRef:
              name: watsonx-ai-secret
              key: project-id
        - name: WATSONX_MODEL_ID
          value: $(params.model-id)
      script: |
        #!/usr/bin/env sh
        set -eu

        raw_status="$(./scripts/capture-error/capture-error.sh \
          --exit-code-only \
          --redaction-regex-file /tmp/capture-redaction-patterns.txt \
          -- ./scripts/capture-error/capture-error-scenarios.sh --all-failure)"

        status="$(printf '%s' "$raw_status" | ./.tools/ai-status-wrapper \
          --config "$(params.wrapper-dir)/config/ai-status-wrapper/config.yaml" \
          --prompts "$(params.wrapper-dir)/config/ai-status-wrapper/prompts" \
          --pipeline "$(params.pipeline)" \
          --prompt-version "$(params.prompt-version)" \
          --timeout 45s \
          --log-level error \
          --redaction-regex-file /tmp/capture-redaction-patterns.txt)"

        printf '%s\n' "$status"
```

Notes for this Task:

- Both steps must run on the same CPU architecture because the first step builds a native Linux binary for the second step.
- The `.tools` directory is written to the shared workspace, not a step-local filesystem.
- The runtime image needs a POSIX shell and CA certificates.
- The runtime namespace needs outbound HTTPS access to the configured IAM and Watson hosts.
- Pin production images to approved immutable versions or digests.
- Compiling on every TaskRun is straightforward but slower than using a versioned binary or container image.

### Store or pass the resulting JSON

Use the enriched `status` exactly where the original status was previously used. If it can be large, prefer a workspace file or object storage over a Tekton result because Tekton result-size limits vary by platform and configuration.

Example workspace file:

```bash
mkdir -p "$(workspaces.source.path)/status"
printf '%s' "$status" > "$(workspaces.source.path)/status/enriched-status.json"
```

### Tekton operational checklist

- Confirm `WATSONX_API_KEY` is available only to the step that needs it.
- Confirm `WATSONX_PROJECT_ID` and `WATSONX_MODEL_ID` resolve to the intended runtime values.
- Disable shell tracing before secrets enter the environment.
- Set an overall wrapper timeout shorter than the Tekton step timeout.
- Allow enough time for up to one IAM request and three sequential Watson calls plus retries.
- Reuse existing capture-error redaction patterns with `--redaction-regex-file`.
- Verify proxy variables and CA trust if the cluster uses an outbound proxy.
- Monitor fallback diagnostics from `stderr` without treating them as command failures.
- Use `--log-level error` for normal CI visibility or `--log-level off` when the surrounding platform supplies sufficient monitoring.
- Test with a known success JSON, known failure JSON, missing API key, and blocked network.
- Avoid writing raw logs or model request bodies to TaskRun annotations or results.

## Prompt development

Prompt packs are selected by `pipeline` and `version`. The current implementation ships `sync/v1`; PR and CD can be added without modifying Go code.

### Required layout

```text
config/ai-status-wrapper/prompts/<pipeline>/<version>/
  stderr/
    fresh.system.md
    fresh.user.md
    fresh.assistant.md        # optional
  stdout/
    fresh.system.md
    fresh.user.md
    fresh.assistant.md        # optional
  final/
    context.system.md
    context.user.md
    context.assistant.md      # optional
  examples/
    known-failure.md          # optional
```

### Available placeholders

Fresh `stderr` and `stdout` prompts receive:

| Placeholder | Value |
| --- | --- |
| `{{command}}` | Captured command display string, if available |
| `{{exit_code}}` | Captured exit code |
| `{{stderr}}` | Prepared stderr for the stderr call |
| `{{stdout}}` | Prepared stdout for the stdout call |
| `{{truncation_note}}` | Whether capture or wrapper reduction occurred |

Final prompts receive:

| Placeholder | Value |
| --- | --- |
| `{{status_summary}}` | Selected status, command, failure, and truncation metadata |
| `{{stderr_analysis}}` | Watson response from the fresh stderr call |
| `{{stdout_analysis}}` | Watson response from the fresh stdout call |
| `{{command}}` | Captured command display string |
| `{{exit_code}}` | Captured exit code |

Any unresolved placeholder causes safe fallback.

When `allow_common_fallback` is enabled, required fallback prompts are resolved without a version directory:

```text
config/ai-status-wrapper/prompts/common/
  stderr/fresh.system.md
  stderr/fresh.user.md
  stdout/fresh.system.md
  stdout/fresh.user.md
  final/context.system.md
  final/context.user.md
```

Common fallback is disabled by default because silently using generic prompts can hide a missing or incorrectly deployed production prompt pack.

### Add a PR prompt pack

```bash
cp -R config/ai-status-wrapper/prompts/sync/v1 \
  config/ai-status-wrapper/prompts/pr/v1
```

Then rewrite the prompt content for PR-specific failures and test selection:

```bash
./bin/ai-status-wrapper \
  --config ./config/ai-status-wrapper/config.yaml \
  --prompts ./config/ai-status-wrapper/prompts \
  --pipeline pr \
  --prompt-version v1 \
  < ./testdata/status/failure.json
```

Do not allow a single prompt pack to cover unrelated pipelines implicitly. Sync, PR, and CD failures have different evidence and remediation patterns.

### Prompt review checklist

- Treat all log and status content as untrusted data, not instructions.
- Require evidence-based conclusions and prohibit invented facts.
- Keep final output concise enough for pipeline logs.
- Avoid asking the model to repeat full logs.
- Keep few-shot examples concise and representative.
- Never place real secrets or customer logs in examples.
- Increment the prompt version for behavior-changing edits.
- Add regression fixtures for repeated real-world failure categories.
- Compare model output quality before changing the default prompt version.

## Security

### Credential handling

- Read the API key only from `WATSONX_API_KEY`.
- Inject it through a Tekton Secret or approved secret manager.
- Supply the deployment project through `WATSONX_PROJECT_ID`; use a Secret or ConfigMap according to organizational policy.
- Select a configured model at runtime with `WATSONX_MODEL_ID`.
- Never add an API-key field to config.
- Never log the API key, IAM form, bearer token, authorization header, or full request body.
- Avoid `set -x`, environment dumps, and debug tooling that records headers.

### Log handling

Logs may contain repository URLs, tokens, file paths, customer identifiers, or command-line secrets. The wrapper applies configurable redaction before external calls, but upstream redaction remains the first defense.

Recommended layers:

1. Redact during capture-error collection.
2. Reuse the same pattern file in the AI wrapper.
3. Add wrapper-specific patterns in config.
4. Limit captured output and wrapper request sizes.
5. Apply IBM service data-governance and retention controls appropriate to the environment.

### Prompt injection

Pipeline logs are untrusted. A failed command can print text that looks like model instructions. System prompts explicitly tell the model to treat logs as evidence rather than instructions. Preserve this rule when adding prompt packs.

### Network and TLS

The wrapper requires absolute HTTPS IAM and Watson endpoints, uses Go's `net/http` TLS verification, and refuses HTTP redirects so credentials and logs cannot be forwarded to a redirect target. Do not disable certificate validation. For private proxies or enterprise CAs, install the approved CA certificate in the runtime image or configure the standard trust store.

## Failure, timeout, and retry behavior

### Timeouts

Three timeout layers exist:

- `--timeout`: overall deadline for configuration-complete enrichment, including all external calls.
- `http.timeout_seconds`: per-request HTTP client timeout.
- `generation.time_limit_ms`: time limit included in each Watson generation request.

Set the overall timeout high enough for three sequential chat calls, but lower than the Tekton step timeout.

### Retries

IAM and Watson clients retry:

- Network request failures.
- HTTP `429`.
- HTTP `5xx`.

They do not retry ordinary `4xx` responses such as `400`, `401`, or `403`. Backoff is exponential based on `retry_backoff_ms`, and `retry_count` is limited to at most 10 by config validation.

If any call exhausts retries, the entire enrichment is discarded and the original input is returned. Partial analysis is never written into the status.

### IAM token cache

The IAM bearer token is cached in memory for the lifetime of one wrapper process. A 30-second safety margin prevents reuse close to expiration. Because a typical CLI invocation processes one document and exits, the cache mainly avoids requesting separate tokens for the three Watson calls.

### Size limits

Logs are reduced before prompt rendering. The Watson client then enforces `body_hard_limit_bytes` on both request and response bodies. An oversized final request or response causes original-input fallback.

## Testing

### Standard checks

```bash
go test ./...
go test -race ./...
go vet ./...
make build
```

Normal test execution uses only local data and `httptest.Server`. The real Watson end-to-end test is skipped unless `RUN_WATSONX_E2E=1` is explicitly set.

### Package test coverage

| Package | Important cases |
| --- | --- |
| `cmd/ai-status-wrapper` | Exact success pass-through, full IAM/three-chat flow, missing-key fallback, opt-in scored live E2E |
| `internal/aistatus` | Four-field classification, required fields, three calls, mutation isolation, chat fallback |
| `internal/config` | YAML subset, unknown fields, invalid model selection, shipped config parsing |
| `internal/logprep` | Regex redaction, pattern-file loading, large-log signal preservation |
| `internal/prompts` | Required/optional files, sorted examples, path traversal, missing placeholders |
| `internal/watsonx` | IAM cache, auth failures, request shape, transient retries, response parsing, body limit |

### Manual smoke tests

Success must remain exactly identical even with missing config:

```bash
./bin/ai-status-wrapper --config /does/not/exist \
  < ./testdata/status/success.json > /tmp/success.out

cmp ./testdata/status/success.json /tmp/success.out
```

Dry-run failure must remain exactly identical:

```bash
./bin/ai-status-wrapper --dry-run \
  < ./testdata/status/failure.json > /tmp/failure.out

cmp ./testdata/status/failure.json /tmp/failure.out
```

### Live Watson end-to-end test

The failure fixtures contain synthetic, non-sensitive logs that model several realistic pipeline failures. The live Go test is opt-in so routine unit tests do not use credentials or network access, consume model quota, or incur costs.

```bash
export WATSONX_API_KEY='...'
export WATSONX_PROJECT_ID='...'
export WATSONX_MODEL_ID='openai/gpt-oss-120b'
export RUN_WATSONX_E2E=1
unset WATSONX_E2E_FIXTURE

go test ./cmd/ai-status-wrapper \
  -run '^TestRealWatsonEndToEndScore$' \
  -count=1 \
  -v
```

By default, the test discovers and sequentially runs every `*.json` file in `testdata/status`. The `success.json` subtest verifies exact byte-for-byte pass-through without calling Watson. Each failure fixture is enriched and scored. To debug only one scenario, set `WATSONX_E2E_FIXTURE` to its file name, for example `failure-rollout-timeout.json`.

When all requests succeed on the first attempt, each failure fixture performs one IAM token request and three Watson chat requests: stderr analysis, stdout analysis, and final synthesis. With the four currently shipped failure fixtures, the default run normally makes four IAM requests and twelve Watson chat requests; retries can increase those counts, and the success fixture makes none.

The test compares the input and output and reports a score out of 100:

- `40` points: every field except `error_message` is semantically unchanged.
- `20` points: `error_message` changed and starts with `AI analysis:`.
- `20` points: the analysis uses meaningful evidence from the input command and logs.
- `10` points: the analysis contains actionable remediation language.
- `10` points: the guidance passes fixture-specific reliability checks, including the expected core diagnosis for each shipped failure fixture and no known misleading remediation or response over 180 words.

The default passing score is `70`. Override it when evaluating a new model or prompt version:

```bash
export WATSONX_E2E_MIN_SCORE=80
```

Field preservation and reliability are mandatory regardless of the configured score. The test logs the scoring breakdown and final AI message, and fails when Watson falls back to the original message, emits known unreliable guidance, or produces an output below the threshold.

#### Example: Why a 90/100 result still fails

The `failure-rollout-timeout.json` fixture models a `kubectl rollout status` command that exits with code `124`, has `timed_out: true`, and reports that an old replica is pending termination. A live Watson response can correctly diagnose the rollout timeout and provide useful investigation steps, but still fail the test if the final developer-facing message is too long. For example:

```text
Watson E2E score: 90/100 (preservation=40/40, message=20/20, evidence=20/20, actionability=10/10, reliability=0/10)
Watson output contains unreliable guidance: response exceeds the 180-word pipeline-log limit; score=90/100
--- FAIL: TestRealWatsonEndToEndScore/failure-rollout-timeout
```

In the observed run, the generated message contained 207 whitespace-separated words. The test uses Go's `strings.Fields` to count words and rejects any message containing more than 180. The corresponding final system prompt also explicitly instructs Watson to keep the complete response at or below 180 words.

This failure is expected test behavior:

- The response earned `40 + 20 + 20 + 10 = 90` points for preservation, message format, evidence, and actionability.
- The length violation reduced reliability from `10` to `0`.
- Reliability is a hard requirement, so a high total score does not override the violation.
- Lowering `WATSONX_E2E_MIN_SCORE` does not make this result pass because the reliability check runs independently of the minimum score.

The failure does not by itself indicate a problem with field preservation, wrapper execution, or the rollout diagnosis. It means the live model output did not satisfy the complete response contract. Because this test calls a generative model, a rerun can produce different wording and length. Repeated failures for the same rule indicate that the selected model or final synthesis prompt needs stronger length control. Possible improvements include tuning the final prompt or examples, validating the generated response and retrying once with an explicit shortening instruction, or selecting a model that follows the limit more consistently. Any shortening mechanism must retain the evidence, root cause, recommended fix, and follow-up checks.

To reproduce or debug only this scenario, keep the Watson credentials and other live-test variables configured, then run:

```bash
export WATSONX_E2E_FIXTURE='failure-rollout-timeout.json'

go test ./cmd/ai-status-wrapper \
  -run '^TestRealWatsonEndToEndScore$' \
  -count=1 \
  -v

unset WATSONX_E2E_FIXTURE
```

When reviewing a failure, use the logged scoring breakdown and `Watson error_message` together. The score identifies which quality dimension failed, while the full message shows whether the problem is excessive length, a missed fixture diagnosis, unsupported speculation, misleading remediation, or an unrelated field change.

Confirm no third-party module was added:

```bash
go list -m all
```

Expected output:

```text
ai-status-wrapper
```

## Troubleshooting

| Symptom or diagnostic | Likely cause | Action |
| --- | --- | --- |
| `watsonx.project_id is required` | Runtime project ID was not injected | Set `WATSONX_PROJECT_ID` in the wrapper step |
| `model ... is not present in model_selection.models` | Runtime model ID is unknown | Set `WATSONX_MODEL_ID` to an ID listed in config |
| `IAM API key is missing` | Secret was not injected or env name is wrong | Set `WATSONX_API_KEY` in the wrapper step |
| IAM HTTP `401` | Invalid or revoked API key | Rotate or correct the Secret |
| IAM or Watson HTTP `403` | Project/service permission issue | Verify IBM IAM roles and project access |
| Watson HTTP `429` | Rate limit or capacity pressure | Review retry settings and service quota |
| Watson HTTP `5xx` | Transient service failure | Wrapper retries, then safely falls back |
| `load required ... prompt` | Wrong `--prompts`, pipeline, version, or missing file | Verify runtime asset paths and prompt pack layout |
| `missing values for ...` | Prompt uses an unsupported placeholder | Correct the template or add a reviewed renderer value |
| `selected model index ... out of range` | Invalid `selected` value | Choose an existing list index |
| Request body exceeds hard limit | Prompt/log context is too large | Lower capture size, improve reduction, or review the hard limit |
| Original failure JSON is returned | Any safe-fallback condition occurred | Inspect `stderr`; run with `--log-level debug` if appropriate |
| No diagnostic and success JSON is unchanged | Expected behavior | Successful status skips all wrapper setup and network calls |
| `exec format error` in Tekton | Binary architecture or OS mismatch | Rebuild for Linux and the worker architecture |
| TLS certificate error | Missing CA certificate or proxy trust | Install the approved CA chain in the runtime image |
| Config parses locally but not after edit | Unsupported YAML feature or tab indentation | Use the documented YAML subset and spaces |

`--log-level debug` reports classification and selected model/prompt pack without printing request bodies or credentials. `--debug` is an equivalent compatibility shortcut:

```bash
./bin/ai-status-wrapper --log-level debug \
  --config ./config/ai-status-wrapper/config.yaml \
  --prompts ./config/ai-status-wrapper/prompts \
  < ./testdata/status/failure.json \
  > /tmp/status.json
```

## Developer maintenance guide

### Normal change workflow

1. Read the safety contract and identify whether the change can affect pass-through behavior.
2. Add or update the smallest relevant package test.
3. Implement the change inside the owning package.
4. Run `gofmt`, `go test ./...`, `go test -race ./...`, and `go vet ./...`.
5. Run both byte-for-byte smoke tests.
6. Confirm `go list -m all` still lists only this module.
7. Update this README, config comments, and prompt versions as needed.

### Add a configuration field

1. Add a typed field with a `json` tag in `internal/config/config.go`.
2. Decide whether zero means default or invalid.
3. Add defaulting and validation.
4. Add it to `config.yaml`.
5. Add valid and invalid tests.
6. Document whether the field is active or reserved.

The YAML parser produces generic maps that are decoded into these JSON-tagged structures with unknown fields rejected. Most new scalar, map, or list fields do not require parser changes.

### Add a model

1. Append the model ID, display name, and context limit to config.
2. Verify generation budgets fit the new limit.
3. Add a selection test.
4. Exercise the model in a non-production environment.
5. Compare response shape and prompt behavior before changing the default index.

### Change the status schema

1. Update parsing and accessors in `internal/aistatus/status.go`.
2. Keep the four-field success rule unless the upstream contract formally changes.
3. Preserve exact original bytes for success and fallback.
4. Preserve unknown fields after enrichment.
5. Add old- and new-schema fixtures to demonstrate backward compatibility.

### Change Watson API behavior

1. Modify only `internal/watsonx` when possible.
2. Keep `ChatClient` stable so orchestration tests remain isolated.
3. Use fake HTTP servers for every new status or response shape.
4. Never use production credentials in tests.
5. Keep retries limited to transient errors.
6. Preserve body limits and credential-safe error messages.

### Change log preparation

Redaction and reduction happen before external calls. Tests should prove:

- Sensitive matches never reach fake Watson requests.
- Original fallback bytes are unchanged.
- Signal lines remain after reduction.
- Prepared context cannot exceed its assigned byte budget.
- UTF-8 and line-boundary behavior remains acceptable for pipeline logs.

### Release checklist

- All tests, race checks, and vet pass.
- No third-party module or import was introduced.
- Version is embedded in the binary.
- Binary targets the intended OS and architecture.
- Artifact checksum is published.
- Config contains no credentials.
- Project ID is supplied through environment-specific deployment config if the template stays generic.
- Prompt pack versions are included and documented.
- Success, AI success, missing-key, timeout, and network-failure scenarios were exercised.
- Rollback artifact and previous prompt pack remain available.

### Compatibility rules worth preserving

- `stdout` contains only status content.
- Runtime logs use `log/slog`, honor the selected level, and write only to `stderr`.
- Successful input is byte-for-byte unchanged.
- Every internal enrichment failure returns original input.
- Successful enrichment changes only `error_message` semantically.
- Unknown JSON fields survive enrichment.
- API key comes only from the environment.
- Prompt selection is explicit and deterministic.
- External requests are bounded by timeout and body limits.
- The module remains standard-library-only.

## Current limitations and future work

- Only the `sync/v1` prompt pack is currently included.
- Watson calls are sequential; the final call depends on both fresh analyses.
- The CLI processes one status document per process.
- IAM token caching is process-local, not shared between invocations.
- Log token estimation uses approximately four bytes per token rather than a model-specific tokenizer.
- Large logs are reduced to beginning, signal lines, and end; they are not analyzed through multiple chunk calls.
- `chunking` settings are reserved for a future multi-chunk implementation.
- Metrics and structured telemetry are not yet emitted.
- At runtime, the final model message is accepted as developer-facing text; richer structured output validation can be added later.
- Prompt assets are runtime files and are not embedded in the binary.
- The internal YAML parser intentionally supports a limited subset.
- Routine tests mock IBM services, while the opt-in live E2E test calls Watson; a separately controlled staging smoke test is still useful before production rollout.

Potential future additions include PR/CD prompt packs, structured metrics for enriched versus fallback outcomes, optional model fallback, stricter final-response schema validation, and signed cross-platform release artifacts. Any enhancement must retain the fail-safe contract.
