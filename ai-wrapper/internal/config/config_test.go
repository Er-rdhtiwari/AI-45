package config

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestLoadAndSelectModel(t *testing.T) {
	path := filepath.Join(t.TempDir(), "config.yaml")
	content := validConfigYAML("1")
	if err := os.WriteFile(path, []byte(content), 0o600); err != nil {
		t.Fatal(err)
	}
	cfg, err := Load(path)
	if err != nil {
		t.Fatalf("Load() error = %v", err)
	}
	if got := cfg.SelectedModel().ID; got != "model-1" {
		t.Fatalf("SelectedModel().ID = %q, want model-1", got)
	}
	if cfg.Generation.FreshMaxInputTokens != 24000 {
		t.Fatalf("default fresh token limit = %d", cfg.Generation.FreshMaxInputTokens)
	}
}

func TestLoadWithRuntimeOverrides(t *testing.T) {
	path := filepath.Join(t.TempDir(), "config.yaml")
	if err := os.WriteFile(path, []byte(validConfigYAML("1")), 0o600); err != nil {
		t.Fatal(err)
	}
	cfg, err := LoadWithOverrides(path, RuntimeOverrides{
		ProjectID: "runtime-project",
		ModelID:   "model-0",
	})
	if err != nil {
		t.Fatalf("LoadWithOverrides() error = %v", err)
	}
	if cfg.WatsonX.ProjectID != "runtime-project" {
		t.Fatalf("ProjectID = %q, want runtime-project", cfg.WatsonX.ProjectID)
	}
	if got := cfg.SelectedModel().ID; got != "model-0" {
		t.Fatalf("SelectedModel().ID = %q, want model-0", got)
	}
}

func TestLoadWithRuntimeOverridesRejectsUnknownModel(t *testing.T) {
	path := filepath.Join(t.TempDir(), "config.yaml")
	if err := os.WriteFile(path, []byte(validConfigYAML("0")), 0o600); err != nil {
		t.Fatal(err)
	}
	_, err := LoadWithOverrides(path, RuntimeOverrides{ModelID: "missing-model"})
	if err == nil || !strings.Contains(err.Error(), "not present in model_selection.models") {
		t.Fatalf("LoadWithOverrides() error = %v, want unknown-model error", err)
	}
}

func TestLoadRejectsUnknownFields(t *testing.T) {
	path := filepath.Join(t.TempDir(), "config.yaml")
	if err := os.WriteFile(path, []byte(validConfigYAML("0")+"unknown: true\n"), 0o600); err != nil {
		t.Fatal(err)
	}
	_, err := Load(path)
	if err == nil || !strings.Contains(err.Error(), `unknown field "unknown"`) {
		t.Fatalf("Load() error = %v, want unknown-field error", err)
	}
}

func TestLoadRejectsInvalidModelSelection(t *testing.T) {
	path := filepath.Join(t.TempDir(), "config.yaml")
	if err := os.WriteFile(path, []byte(validConfigYAML("2")), 0o600); err != nil {
		t.Fatal(err)
	}
	_, err := Load(path)
	if err == nil || !strings.Contains(err.Error(), "out of range") {
		t.Fatalf("Load() error = %v, want out-of-range error", err)
	}
}

func validConfigYAML(selected string) string {
	return `watsonx:
  url: "https://watson.example"
  api_version: "2024-05-31"
  project_id: "project"
  iam_token_url: "https://iam.example/token"
model_selection:
  selected: ` + selected + `
  models:
    - id: "model-0"
      context_limit_tokens: 131072
    - id: "model-1"
      context_limit_tokens: 131072
prompting:
  pipeline: "sync"
  version: "v1"
http:
  timeout_seconds: 1
  retry_count: 0
  retry_backoff_ms: 1
  body_warning_bytes: 1000
  body_hard_limit_bytes: 2000
chunking:
  chunk_size_tokens: 100
  chunk_overlap_tokens: 10
fallback:
  return_original_on_ai_error: true
  return_original_on_config_error: true
`
}
