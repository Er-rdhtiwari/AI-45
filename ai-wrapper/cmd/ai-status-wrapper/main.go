package main

import (
	"context"
	"errors"
	"flag"
	"fmt"
	"io"
	"log/slog"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"time"

	"ai-status-wrapper/internal/aistatus"
	"ai-status-wrapper/internal/config"
	"ai-status-wrapper/internal/logprep"
	"ai-status-wrapper/internal/prompts"
	"ai-status-wrapper/internal/watsonx"
)

var version = "dev"

const logLevelEnvironment = "AI_STATUS_WRAPPER_LOG_LEVEL"

const (
	projectIDEnvironment = "WATSONX_PROJECT_ID"
	modelIDEnvironment   = "WATSONX_MODEL_ID"
)

const maxInputBytes = 10 * 1024 * 1024

func main() {
	os.Exit(run(os.Args[1:], os.Stdin, os.Stdout, os.Stderr))
}

func run(args []string, stdin io.Reader, stdout, stderr io.Writer) int {
	return runWithHTTPClient(args, stdin, stdout, stderr, nil)
}

func runWithHTTPClient(args []string, stdin io.Reader, stdout, stderr io.Writer, httpClient *http.Client) int {
	flags := flag.NewFlagSet("ai-status-wrapper", flag.ContinueOnError)
	flags.SetOutput(stderr)
	configPath := flags.String("config", "./config/ai-status-wrapper/config.yaml", "path to YAML configuration")
	promptsPath := flags.String("prompts", "./config/ai-status-wrapper/prompts", "root directory containing prompt packs")
	inputPath := flags.String("input", "", "optional input file (defaults to stdin)")
	outputPath := flags.String("output", "", "optional output file (defaults to stdout)")
	pipeline := flags.String("pipeline", "", "prompt pipeline override, such as sync, pr, or cd")
	promptVersion := flags.String("prompt-version", "", "prompt version override, such as v1")
	timeout := flags.Duration("timeout", 60*time.Second, "overall wrapper timeout")
	redactionFile := flags.String("redaction-regex-file", "", "optional newline-delimited redaction regex file")
	dryRun := flags.Bool("dry-run", false, "parse and classify without calling Watson")
	logLevel := flags.String("log-level", defaultLogLevel(), "logging level: off, error, info, or debug")
	debug := flags.Bool("debug", false, "compatibility shortcut for --log-level=debug")
	showVersion := flags.Bool("version", false, "print version and exit")
	if err := flags.Parse(args); err != nil {
		return 2
	}
	selectedLogLevel := *logLevel
	if *debug {
		selectedLogLevel = "debug"
	}
	logger, err := newLogger(stderr, selectedLogLevel)
	if err != nil {
		bootstrapLogger := slog.New(slog.NewTextHandler(stderr, &slog.HandlerOptions{Level: slog.LevelError}))
		bootstrapLogger.Error("invalid log level", "value", selectedLogLevel, "error", err)
		return 2
	}
	logger.Debug("logger initialized", "configured_level", strings.ToLower(strings.TrimSpace(selectedLogLevel)))
	if flags.NArg() != 0 {
		logger.Error("unexpected positional arguments", "count", flags.NArg())
		return 2
	}
	if *showVersion {
		if _, err := io.WriteString(stdout, version+"\n"); err != nil {
			logger.Error("cannot write version output", "error", err)
			return 1
		}
		return 0
	}

	input, err := readInput(*inputPath, stdin)
	if err != nil {
		logger.Error("cannot read input", "error", err)
		return 1
	}
	doc, err := aistatus.Parse(input)
	if err != nil {
		inputFallbackDiagnostic(logger, err)
		return emit(input, *outputPath, stdout, logger)
	}
	logger.Debug("status JSON parsed", "successful", doc.IsSuccessful())
	if doc.IsSuccessful() {
		logger.Info("input classified as success; Watson call skipped")
		return emit(input, *outputPath, stdout, logger)
	}
	if *dryRun {
		logger.Info("input classified as failure; dry-run skipped Watson calls")
		return emit(input, *outputPath, stdout, logger)
	}

	cfg, err := config.LoadWithOverrides(*configPath, config.RuntimeOverrides{
		ProjectID: os.Getenv(projectIDEnvironment),
		ModelID:   os.Getenv(modelIDEnvironment),
	})
	if err != nil {
		fallbackDiagnostic(logger, err)
		return emit(input, *outputPath, stdout, logger)
	}
	if *pipeline != "" {
		cfg.Prompting.Pipeline = *pipeline
	}
	if *promptVersion != "" {
		cfg.Prompting.Version = *promptVersion
	}
	if *timeout <= 0 {
		fallbackDiagnostic(logger, errors.New("overall timeout must be positive"))
		return emit(input, *outputPath, stdout, logger)
	}
	logger.Debug("configuration loaded",
		"model_id", cfg.SelectedModel().ID,
		"pipeline", cfg.Prompting.Pipeline,
		"prompt_version", cfg.Prompting.Version,
	)

	filePatterns, err := logprep.PatternsFromFile(*redactionFile)
	if err != nil {
		fallbackDiagnostic(logger, err)
		return emit(input, *outputPath, stdout, logger)
	}
	allPatterns := append([]string{}, cfg.Security.RedactionPatterns...)
	allPatterns = append(allPatterns, filePatterns...)
	sanitizer, err := logprep.NewSanitizer(allPatterns)
	if err != nil {
		fallbackDiagnostic(logger, err)
		return emit(input, *outputPath, stdout, logger)
	}

	if httpClient == nil {
		httpClient = &http.Client{}
	} else {
		clone := *httpClient
		httpClient = &clone
	}
	httpClient.Timeout = time.Duration(cfg.HTTP.TimeoutSeconds) * time.Second
	iam := watsonx.NewIAMClient(
		cfg.WatsonX.IAMTokenURL,
		os.Getenv("WATSONX_API_KEY"),
		httpClient,
		cfg.HTTP.RetryCount,
		time.Duration(cfg.HTTP.RetryBackoffMS)*time.Millisecond,
	)
	chat, err := watsonx.NewClient(watsonx.ClientOptions{
		BaseURL:       cfg.WatsonX.URL,
		APIVersion:    cfg.WatsonX.APIVersion,
		ModelID:       cfg.SelectedModel().ID,
		ProjectID:     cfg.WatsonX.ProjectID,
		Tokens:        iam,
		HTTPClient:    httpClient,
		Retries:       cfg.HTTP.RetryCount,
		Backoff:       time.Duration(cfg.HTTP.RetryBackoffMS) * time.Millisecond,
		HardBodyLimit: cfg.HTTP.BodyHardLimitBytes,
	})
	if err != nil {
		fallbackDiagnostic(logger, err)
		return emit(input, *outputPath, stdout, logger)
	}
	processor := &aistatus.Processor{
		Config: cfg,
		Prompts: prompts.Loader{
			Root:                *promptsPath,
			Pipeline:            cfg.Prompting.Pipeline,
			Version:             cfg.Prompting.Version,
			AllowCommonFallback: cfg.Prompting.AllowCommonFallback,
			EnableFewShot:       cfg.Prompting.EnableFewShot,
			MaxExamples:         cfg.Prompting.MaxExamplesPerCall,
		},
		Chat:      chat,
		Sanitizer: sanitizer,
	}
	ctx, cancel := context.WithTimeout(context.Background(), *timeout)
	defer cancel()
	result, err := processor.Enrich(ctx, doc)
	if err != nil {
		fallbackDiagnostic(logger, err)
		result = input
	} else {
		logger.Info("failure status enriched",
			"model_id", cfg.SelectedModel().ID,
			"pipeline", cfg.Prompting.Pipeline,
			"prompt_version", cfg.Prompting.Version,
		)
	}
	return emit(result, *outputPath, stdout, logger)
}

func readInput(path string, stdin io.Reader) ([]byte, error) {
	if strings.TrimSpace(path) == "" {
		return readLimitedInput(stdin)
	}
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()
	return readLimitedInput(file)
}

func readLimitedInput(reader io.Reader) ([]byte, error) {
	limited := &io.LimitedReader{R: reader, N: maxInputBytes + 1}
	input, err := io.ReadAll(limited)
	if err != nil {
		return nil, err
	}
	if len(input) > maxInputBytes {
		return nil, fmt.Errorf("input exceeds %d-byte limit", maxInputBytes)
	}
	return input, nil
}

func emit(result []byte, path string, stdout io.Writer, logger *slog.Logger) int {
	var err error
	if strings.TrimSpace(path) == "" {
		_, err = stdout.Write(result)
	} else {
		err = writePrivateFile(path, result)
	}
	if err != nil {
		logger.Error("cannot write output", "error", err)
		return 1
	}
	return 0
}

func writePrivateFile(path string, result []byte) error {
	directory := filepath.Dir(path)
	temporary, err := os.CreateTemp(directory, "."+filepath.Base(path)+"-*")
	if err != nil {
		return err
	}
	temporaryPath := temporary.Name()
	defer os.Remove(temporaryPath)
	if err := temporary.Chmod(0o600); err != nil {
		temporary.Close()
		return err
	}
	if _, err := temporary.Write(result); err != nil {
		temporary.Close()
		return err
	}
	if err := temporary.Close(); err != nil {
		return err
	}
	return os.Rename(temporaryPath, path)
}

func fallbackDiagnostic(logger *slog.Logger, err error) {
	logger.Error("enrichment unavailable; returning original input", "error", err)
}

func inputFallbackDiagnostic(logger *slog.Logger, err error) {
	logger.Error("status input invalid; returning original input", "error", err)
}

func defaultLogLevel() string {
	level := strings.TrimSpace(os.Getenv(logLevelEnvironment))
	if level == "" {
		return "error"
	}
	return level
}

func newLogger(output io.Writer, rawLevel string) (*slog.Logger, error) {
	var level slog.Level
	switch strings.ToLower(strings.TrimSpace(rawLevel)) {
	case "off":
		return slog.New(slog.NewTextHandler(io.Discard, nil)).With("component", "ai-status-wrapper"), nil
	case "error":
		level = slog.LevelError
	case "info":
		level = slog.LevelInfo
	case "debug":
		level = slog.LevelDebug
	default:
		return nil, errors.New("level must be one of: off, error, info, debug")
	}
	handler := slog.NewTextHandler(output, &slog.HandlerOptions{Level: level})
	return slog.New(handler).With("component", "ai-status-wrapper"), nil
}
