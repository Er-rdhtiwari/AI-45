package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"strings"
	"sync/atomic"
	"testing"
)

func TestRunSuccessIsExactPassThroughWithoutConfiguration(t *testing.T) {
	input := []byte(" {\n\"success\":true,\"status\":\"success\",\"exit_code\":0,\"wrapper_exit_code\":0\n}\n")
	var stdout, stderr bytes.Buffer
	exit := run([]string{"--config", filepath.Join(t.TempDir(), "missing.yaml")}, bytes.NewReader(input), &stdout, &stderr)
	if exit != 0 {
		t.Fatalf("run() exit = %d, stderr=%s", exit, stderr.String())
	}
	if !bytes.Equal(stdout.Bytes(), input) {
		t.Fatalf("stdout changed:\n%s", stdout.Bytes())
	}
	if stderr.Len() != 0 {
		t.Fatalf("unexpected stderr: %s", stderr.String())
	}
}

func TestRunDryRunFailureSkipsRuntimeDependencies(t *testing.T) {
	input := []byte(" {\n\"success\":false,\"status\":\"failed\",\"exit_code\":1,\"wrapper_exit_code\":1,\"output\":{\"stdout\":\"out\",\"stderr\":\"err\"}\n}\n")
	var stdout, stderr bytes.Buffer
	exit := run([]string{
		"--dry-run",
		"--log-level", "info",
		"--config", filepath.Join(t.TempDir(), "missing.yaml"),
		"--prompts", filepath.Join(t.TempDir(), "missing-prompts"),
	}, bytes.NewReader(input), &stdout, &stderr)
	if exit != 0 {
		t.Fatalf("run() exit = %d, stderr=%s", exit, stderr.String())
	}
	if !bytes.Equal(stdout.Bytes(), input) {
		t.Fatalf("dry-run changed input:\n%s", stdout.Bytes())
	}
	if !strings.Contains(stderr.String(), "input classified as failure; dry-run skipped Watson calls") {
		t.Fatalf("dry-run diagnostic missing: %s", stderr.String())
	}
	if strings.Contains(stderr.String(), "missing.yaml") || strings.Contains(stderr.String(), "missing-prompts") {
		t.Fatalf("dry-run accessed runtime dependencies: %s", stderr.String())
	}
}

func TestRunDryRunInvalidInputReturnsExactInputWithAccurateDiagnostic(t *testing.T) {
	input := []byte("{not-json}\n")
	var stdout, stderr bytes.Buffer
	exit := run([]string{"--dry-run"}, bytes.NewReader(input), &stdout, &stderr)
	if exit != 0 {
		t.Fatalf("run() exit = %d, stderr=%s", exit, stderr.String())
	}
	if !bytes.Equal(stdout.Bytes(), input) {
		t.Fatalf("invalid-input fallback changed bytes: %q", stdout.Bytes())
	}
	if !strings.Contains(stderr.String(), "status input invalid; returning original input") ||
		strings.Contains(stderr.String(), "enrichment unavailable") {
		t.Fatalf("invalid-input diagnostic is misleading: %s", stderr.String())
	}
}

func TestRunFailureUsesIAMAndThreeWatsonCalls(t *testing.T) {
	var iamCalls, chatCalls atomic.Int32
	server := httptest.NewTLSServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		switch r.URL.Path {
		case "/identity/token":
			iamCalls.Add(1)
			if err := r.ParseForm(); err != nil {
				t.Error(err)
			}
			if r.Form.Get("apikey") != "test-api-key" {
				t.Errorf("apikey = %q", r.Form.Get("apikey"))
			}
			fmt.Fprint(w, `{"access_token":"token","expires_in":3600}`)
		case "/ml/v1/text/chat":
			call := chatCalls.Add(1)
			if r.Header.Get("Authorization") != "Bearer token" {
				t.Errorf("Authorization = %q", r.Header.Get("Authorization"))
			}
			var request struct {
				ModelID   string `json:"model_id"`
				ProjectID string `json:"project_id"`
			}
			if err := json.NewDecoder(r.Body).Decode(&request); err != nil {
				t.Error(err)
			}
			if request.ModelID != "model-zero" || request.ProjectID != "runtime-project" {
				t.Errorf("runtime config = model %q, project %q", request.ModelID, request.ProjectID)
			}
			content := "analysis"
			if call == 3 {
				content = "Main issue: missing executable. Recommended fix: install it."
			}
			fmt.Fprintf(w, `{"choices":[{"message":{"content":%q}}]}`, content)
		default:
			http.NotFound(w, r)
		}
	}))
	defer server.Close()

	configPath := filepath.Join(t.TempDir(), "config.yaml")
	configText := fmt.Sprintf(`watsonx:
  url: %q
  api_version: "2024-05-31"
  project_id: "project"
  iam_token_url: %q
model_selection:
  selected: 1
  models:
    - id: "model-zero"
      context_limit_tokens: 10000
    - id: "model-one"
      context_limit_tokens: 10000
prompting:
  pipeline: "sync"
  version: "v1"
  allow_common_fallback: false
  enable_few_shot: false
  max_examples_per_call: 0
generation:
  fresh_max_input_tokens: 1000
  fresh_max_output_tokens: 100
  final_max_total_input_tokens: 2000
  final_max_output_tokens: 100
  time_limit_ms: 1000
http:
  timeout_seconds: 2
  retry_count: 0
  retry_backoff_ms: 1
  body_warning_bytes: 500000
  body_hard_limit_bytes: 1000000
chunking:
  chunk_size_tokens: 100
  chunk_overlap_tokens: 10
fallback:
  return_original_on_ai_error: true
  return_original_on_config_error: true
`, server.URL, server.URL+"/identity/token")
	if err := os.WriteFile(configPath, []byte(configText), 0o600); err != nil {
		t.Fatal(err)
	}
	t.Setenv("WATSONX_API_KEY", "test-api-key")
	t.Setenv("WATSONX_PROJECT_ID", "runtime-project")
	t.Setenv("WATSONX_MODEL_ID", "model-zero")
	input := []byte(`{"success":false,"status":"failed","exit_code":127,"wrapper_exit_code":127,"error_message":"original","command":{"display":"missing-tool"},"summary":{"stdout_truncated":false,"stderr_truncated":false},"output":{"stdout":"starting","stderr":"not found"},"preserve_me":42}`)
	var stdout, stderr bytes.Buffer
	exit := runWithHTTPClient([]string{
		"--config", configPath,
		"--prompts", filepath.Join("..", "..", "config", "ai-status-wrapper", "prompts"),
		"--timeout", "5s",
	}, bytes.NewReader(input), &stdout, &stderr, server.Client())
	if exit != 0 {
		t.Fatalf("run() exit = %d, stderr=%s", exit, stderr.String())
	}
	if iamCalls.Load() != 1 || chatCalls.Load() != 3 {
		t.Fatalf("IAM calls=%d, chat calls=%d; want 1 and 3", iamCalls.Load(), chatCalls.Load())
	}
	var result map[string]any
	if err := json.Unmarshal(stdout.Bytes(), &result); err != nil {
		t.Fatalf("invalid output JSON: %v\n%s", err, stdout.String())
	}
	if !strings.HasPrefix(result["error_message"].(string), "AI analysis: Main issue") {
		t.Fatalf("error_message = %q", result["error_message"])
	}
	if result["preserve_me"] != float64(42) {
		t.Fatalf("unknown field was not preserved: %#v", result)
	}
	if stderr.Len() != 0 {
		t.Fatalf("unexpected stderr: %s", stderr.String())
	}
}

func TestRunFailureFallsBackOnMissingAPIKey(t *testing.T) {
	shippedConfig := filepath.Join("..", "..", "config", "ai-status-wrapper", "config.yaml")
	configBytes, err := os.ReadFile(shippedConfig)
	if err != nil {
		t.Fatal(err)
	}
	configPath := filepath.Join(t.TempDir(), "config.yaml")
	if err := os.WriteFile(configPath, configBytes, 0o600); err != nil {
		t.Fatal(err)
	}
	input := []byte(`{"success":false,"status":"failed","exit_code":1,"wrapper_exit_code":1,"output":{"stdout":"","stderr":"failed"}}`)
	t.Setenv("WATSONX_API_KEY", "")
	t.Setenv("WATSONX_PROJECT_ID", "test-project")
	var stdout, stderr bytes.Buffer
	exit := run([]string{
		"--config", configPath,
		"--prompts", filepath.Join("..", "..", "config", "ai-status-wrapper", "prompts"),
	}, bytes.NewReader(input), &stdout, &stderr)
	if exit != 0 || !bytes.Equal(stdout.Bytes(), input) {
		t.Fatalf("run() exit=%d stdout=%q stderr=%q", exit, stdout.String(), stderr.String())
	}
	if !strings.Contains(stderr.String(), "level=ERROR") || !strings.Contains(stderr.String(), "component=ai-status-wrapper") ||
		!strings.Contains(stderr.String(), "IAM API key is missing") || !strings.Contains(stderr.String(), "returning original input") {
		t.Fatalf("fallback diagnostic missing: %s", stderr.String())
	}
}

func TestRunLogLevels(t *testing.T) {
	successInput := []byte(`{"success":true,"status":"success","exit_code":0,"wrapper_exit_code":0}`)
	tests := []struct {
		name         string
		args         []string
		wantLogParts []string
		wantNoLogs   bool
	}{
		{name: "off", args: []string{"--log-level", "off"}, wantNoLogs: true},
		{name: "error filters info", args: []string{"--log-level", "error"}, wantNoLogs: true},
		{name: "info", args: []string{"--log-level", "info"}, wantLogParts: []string{"level=INFO", `msg="input classified as success; Watson call skipped"`, "component=ai-status-wrapper"}},
		{name: "debug", args: []string{"--log-level", "debug"}, wantLogParts: []string{"level=DEBUG", `msg="logger initialized"`, `configured_level=debug`, `msg="status JSON parsed"`}},
		{name: "debug compatibility flag", args: []string{"--log-level", "off", "--debug"}, wantLogParts: []string{"level=DEBUG", `configured_level=debug`}},
	}
	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			var stdout, stderr bytes.Buffer
			exit := run(test.args, bytes.NewReader(successInput), &stdout, &stderr)
			if exit != 0 {
				t.Fatalf("run() exit=%d stderr=%s", exit, stderr.String())
			}
			if !bytes.Equal(stdout.Bytes(), successInput) {
				t.Fatalf("logging changed stdout: %q", stdout.String())
			}
			if test.wantNoLogs && stderr.Len() != 0 {
				t.Fatalf("stderr=%q, want no logs", stderr.String())
			}
			for _, part := range test.wantLogParts {
				if !strings.Contains(stderr.String(), part) {
					t.Fatalf("stderr missing %q:\n%s", part, stderr.String())
				}
			}
		})
	}
}

func TestRunLogLevelFromEnvironment(t *testing.T) {
	t.Setenv(logLevelEnvironment, "info")
	input := []byte(`{"success":true,"status":"success","exit_code":0,"wrapper_exit_code":0}`)
	var stdout, stderr bytes.Buffer
	exit := run(nil, bytes.NewReader(input), &stdout, &stderr)
	if exit != 0 || !strings.Contains(stderr.String(), "level=INFO") {
		t.Fatalf("run() exit=%d stderr=%q", exit, stderr.String())
	}
}

func TestRunOffSuppressesFallbackLogging(t *testing.T) {
	input := []byte("not-json")
	var stdout, stderr bytes.Buffer
	exit := run([]string{"--log-level", "off"}, bytes.NewReader(input), &stdout, &stderr)
	if exit != 0 || !bytes.Equal(stdout.Bytes(), input) {
		t.Fatalf("run() exit=%d stdout=%q", exit, stdout.String())
	}
	if stderr.Len() != 0 {
		t.Fatalf("stderr=%q, want logging disabled", stderr.String())
	}
}

func TestRunRejectsInvalidLogLevel(t *testing.T) {
	var stdout, stderr bytes.Buffer
	exit := run([]string{"--log-level", "verbose"}, strings.NewReader(""), &stdout, &stderr)
	if exit != 2 {
		t.Fatalf("run() exit=%d, want 2", exit)
	}
	for _, part := range []string{"level=ERROR", `msg="invalid log level"`, "value=verbose"} {
		if !strings.Contains(stderr.String(), part) {
			t.Fatalf("stderr missing %q: %s", part, stderr.String())
		}
	}
}

func TestReadInputRejectsOversizedInput(t *testing.T) {
	_, err := readInput("", strings.NewReader(strings.Repeat("x", maxInputBytes+1)))
	if err == nil || !strings.Contains(err.Error(), "input exceeds") {
		t.Fatalf("readInput() error = %v", err)
	}
}

func TestWritePrivateFileUsesPrivateModeAndDoesNotFollowSymlink(t *testing.T) {
	directory := t.TempDir()
	target := filepath.Join(directory, "target")
	output := filepath.Join(directory, "output")
	if err := os.WriteFile(target, []byte("keep"), 0o644); err != nil {
		t.Fatal(err)
	}
	if err := os.Symlink(target, output); err != nil {
		t.Fatal(err)
	}
	if err := writePrivateFile(output, []byte("result")); err != nil {
		t.Fatal(err)
	}
	targetBytes, err := os.ReadFile(target)
	if err != nil {
		t.Fatal(err)
	}
	if string(targetBytes) != "keep" {
		t.Fatalf("symlink target was overwritten: %q", targetBytes)
	}
	info, err := os.Stat(output)
	if err != nil {
		t.Fatal(err)
	}
	if info.Mode().Perm() != 0o600 {
		t.Fatalf("output mode = %o, want 600", info.Mode().Perm())
	}
}
