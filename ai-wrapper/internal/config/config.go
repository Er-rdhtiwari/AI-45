package config

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"os"
	"strings"
)

// Config contains all runtime settings. Credentials deliberately do not belong
// here; the Watson API key is read from WATSONX_API_KEY by the CLI.
type Config struct {
	WatsonX        WatsonXConfig        `json:"watsonx"`
	ModelSelection ModelSelectionConfig `json:"model_selection"`
	Prompting      PromptingConfig      `json:"prompting"`
	Generation     GenerationConfig     `json:"generation"`
	HTTP           HTTPConfig           `json:"http"`
	Chunking       ChunkingConfig       `json:"chunking"`
	Security       SecurityConfig       `json:"security"`
	Fallback       FallbackConfig       `json:"fallback"`
}

type WatsonXConfig struct {
	URL         string `json:"url"`
	APIVersion  string `json:"api_version"`
	ProjectID   string `json:"project_id"`
	IAMTokenURL string `json:"iam_token_url"`
}

type ModelSelectionConfig struct {
	Selected int           `json:"selected"`
	Models   []ModelConfig `json:"models"`
}

type ModelConfig struct {
	ID                 string `json:"id"`
	Name               string `json:"name"`
	ContextLimitTokens int    `json:"context_limit_tokens"`
}

type PromptingConfig struct {
	Pipeline            string `json:"pipeline"`
	Version             string `json:"version"`
	AllowCommonFallback bool   `json:"allow_common_fallback"`
	EnableFewShot       bool   `json:"enable_few_shot"`
	MaxExamplesPerCall  int    `json:"max_examples_per_call"`
	MetricsLabel        string `json:"metrics_label"`
}

type GenerationConfig struct {
	DefaultMaxOutputTokens   int `json:"default_max_output_tokens"`
	FreshMaxInputTokens      int `json:"fresh_max_input_tokens"`
	FreshMaxOutputTokens     int `json:"fresh_max_output_tokens"`
	FinalMaxTotalInputTokens int `json:"final_max_total_input_tokens"`
	FinalMaxOutputTokens     int `json:"final_max_output_tokens"`
	TimeLimitMS              int `json:"time_limit_ms"`
}

type HTTPConfig struct {
	TimeoutSeconds     int `json:"timeout_seconds"`
	RetryCount         int `json:"retry_count"`
	RetryBackoffMS     int `json:"retry_backoff_ms"`
	BodyWarningBytes   int `json:"body_warning_bytes"`
	BodyHardLimitBytes int `json:"body_hard_limit_bytes"`
}

type ChunkingConfig struct {
	ChunkSizeTokens    int `json:"chunk_size_tokens"`
	ChunkOverlapTokens int `json:"chunk_overlap_tokens"`
}

type SecurityConfig struct {
	RedactionPatterns []string `json:"redaction_patterns"`
}

type FallbackConfig struct {
	ReturnOriginalOnAIError     bool `json:"return_original_on_ai_error"`
	ReturnOriginalOnConfigError bool `json:"return_original_on_config_error"`
}

// RuntimeOverrides contains deployment-specific values supplied by the CLI.
// Empty values leave the YAML defaults unchanged.
type RuntimeOverrides struct {
	ProjectID string
	ModelID   string
}

func Load(path string) (Config, error) {
	return LoadWithOverrides(path, RuntimeOverrides{})
}

func LoadWithOverrides(path string, overrides RuntimeOverrides) (Config, error) {
	b, err := os.ReadFile(path)
	if err != nil {
		return Config{}, fmt.Errorf("read config: %w", err)
	}

	raw, err := parseYAML(b)
	if err != nil {
		return Config{}, fmt.Errorf("decode config: %w", err)
	}
	encoded, err := json.Marshal(raw)
	if err != nil {
		return Config{}, fmt.Errorf("decode config: convert parsed YAML: %w", err)
	}
	var cfg Config
	dec := json.NewDecoder(bytes.NewReader(encoded))
	dec.DisallowUnknownFields()
	if err := dec.Decode(&cfg); err != nil {
		return Config{}, fmt.Errorf("decode config: %w", err)
	}
	var extra any
	if err := dec.Decode(&extra); !errors.Is(err, io.EOF) {
		if err == nil {
			return Config{}, errors.New("decode config: multiple configuration values are not allowed")
		}
		return Config{}, fmt.Errorf("decode config trailing value: %w", err)
	}
	applyDefaults(&cfg)
	if err := applyRuntimeOverrides(&cfg, overrides); err != nil {
		return Config{}, err
	}
	if err := cfg.Validate(); err != nil {
		return Config{}, err
	}
	return cfg, nil
}

func applyRuntimeOverrides(cfg *Config, overrides RuntimeOverrides) error {
	if projectID := strings.TrimSpace(overrides.ProjectID); projectID != "" {
		cfg.WatsonX.ProjectID = projectID
	}
	if modelID := strings.TrimSpace(overrides.ModelID); modelID != "" {
		for index, model := range cfg.ModelSelection.Models {
			if model.ID == modelID {
				cfg.ModelSelection.Selected = index
				return nil
			}
		}
		return fmt.Errorf("apply runtime config: model %q is not present in model_selection.models", modelID)
	}
	return nil
}

func applyDefaults(cfg *Config) {
	if cfg.Generation.DefaultMaxOutputTokens == 0 {
		cfg.Generation.DefaultMaxOutputTokens = 4096
	}
	if cfg.Generation.FreshMaxInputTokens == 0 {
		cfg.Generation.FreshMaxInputTokens = 24000
	}
	if cfg.Generation.FreshMaxOutputTokens == 0 {
		cfg.Generation.FreshMaxOutputTokens = cfg.Generation.DefaultMaxOutputTokens
	}
	if cfg.Generation.FinalMaxTotalInputTokens == 0 {
		cfg.Generation.FinalMaxTotalInputTokens = 64000
	}
	if cfg.Generation.FinalMaxOutputTokens == 0 {
		cfg.Generation.FinalMaxOutputTokens = cfg.Generation.DefaultMaxOutputTokens
	}
	if cfg.Generation.TimeLimitMS == 0 {
		cfg.Generation.TimeLimitMS = 10000
	}
	if cfg.HTTP.TimeoutSeconds == 0 {
		cfg.HTTP.TimeoutSeconds = 30
	}
	if cfg.HTTP.RetryBackoffMS == 0 {
		cfg.HTTP.RetryBackoffMS = 500
	}
	if cfg.HTTP.BodyWarningBytes == 0 {
		cfg.HTTP.BodyWarningBytes = 512 * 1024
	}
	if cfg.HTTP.BodyHardLimitBytes == 0 {
		cfg.HTTP.BodyHardLimitBytes = 1024 * 1024
	}
	if cfg.Chunking.ChunkSizeTokens == 0 {
		cfg.Chunking.ChunkSizeTokens = 1024
	}
	if cfg.Chunking.ChunkOverlapTokens == 0 {
		cfg.Chunking.ChunkOverlapTokens = 128
	}
}

func (c Config) Validate() error {
	required := map[string]string{
		"watsonx.url":           c.WatsonX.URL,
		"watsonx.api_version":   c.WatsonX.APIVersion,
		"watsonx.project_id":    c.WatsonX.ProjectID,
		"watsonx.iam_token_url": c.WatsonX.IAMTokenURL,
		"prompting.pipeline":    c.Prompting.Pipeline,
		"prompting.version":     c.Prompting.Version,
	}
	for name, value := range required {
		if strings.TrimSpace(value) == "" {
			return fmt.Errorf("validate config: %s is required", name)
		}
	}
	if strings.Contains(c.WatsonX.ProjectID, "<") {
		return errors.New("validate config: watsonx.project_id still contains a placeholder")
	}
	if len(c.ModelSelection.Models) == 0 {
		return errors.New("validate config: model_selection.models must not be empty")
	}
	if c.ModelSelection.Selected < 0 || c.ModelSelection.Selected >= len(c.ModelSelection.Models) {
		return fmt.Errorf("validate config: selected model index %d is out of range", c.ModelSelection.Selected)
	}
	for i, model := range c.ModelSelection.Models {
		if strings.TrimSpace(model.ID) == "" {
			return fmt.Errorf("validate config: model %d id is required", i)
		}
		if model.ContextLimitTokens <= 0 {
			return fmt.Errorf("validate config: model %d context_limit_tokens must be positive", i)
		}
	}
	if c.HTTP.TimeoutSeconds <= 0 || c.HTTP.RetryCount < 0 || c.HTTP.RetryCount > 10 || c.HTTP.RetryBackoffMS < 0 {
		return errors.New("validate config: invalid HTTP timeout or retry settings")
	}
	if c.HTTP.BodyHardLimitBytes <= 0 || c.HTTP.BodyWarningBytes > c.HTTP.BodyHardLimitBytes {
		return errors.New("validate config: invalid HTTP body limits")
	}
	if c.Generation.FreshMaxInputTokens <= 0 || c.Generation.FreshMaxOutputTokens <= 0 ||
		c.Generation.FinalMaxTotalInputTokens <= 0 || c.Generation.FinalMaxOutputTokens <= 0 ||
		c.Generation.TimeLimitMS <= 0 {
		return errors.New("validate config: generation token and time limits must be positive")
	}
	if c.Chunking.ChunkSizeTokens <= 0 || c.Chunking.ChunkOverlapTokens < 0 ||
		c.Chunking.ChunkOverlapTokens >= c.Chunking.ChunkSizeTokens {
		return errors.New("validate config: chunk overlap must be non-negative and smaller than chunk size")
	}
	if c.Prompting.MaxExamplesPerCall < 0 {
		return errors.New("validate config: max_examples_per_call must be non-negative")
	}
	modelLimit := c.SelectedModel().ContextLimitTokens
	if c.Generation.FreshMaxInputTokens+c.Generation.FreshMaxOutputTokens > modelLimit {
		return errors.New("validate config: fresh input and output limits exceed selected model context")
	}
	if c.Generation.FinalMaxTotalInputTokens+c.Generation.FinalMaxOutputTokens > modelLimit {
		return errors.New("validate config: final input and output limits exceed selected model context")
	}
	return nil
}

func (c Config) SelectedModel() ModelConfig {
	return c.ModelSelection.Models[c.ModelSelection.Selected]
}
