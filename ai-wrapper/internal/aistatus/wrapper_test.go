package aistatus

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"path/filepath"
	"reflect"
	"strings"
	"testing"

	"ai-status-wrapper/internal/config"
	"ai-status-wrapper/internal/logprep"
	"ai-status-wrapper/internal/prompts"
	"ai-status-wrapper/internal/watsonx"
)

type fakeChat struct {
	calls     [][]watsonx.Message
	responses []string
	failAt    int
}

func (f *fakeChat) Chat(_ context.Context, messages []watsonx.Message, _, _ int) (string, error) {
	f.calls = append(f.calls, messages)
	if f.failAt > 0 && len(f.calls) == f.failAt {
		return "", errors.New("injected chat failure")
	}
	return f.responses[len(f.calls)-1], nil
}

func TestProcessorSuccessReturnsExactOriginalWithoutChat(t *testing.T) {
	input := []byte(" {\n \"success\": true, \"status\": \"success\", \"exit_code\": 0, \"wrapper_exit_code\": 0\n}\n")
	chat := &fakeChat{}
	processor := &Processor{Chat: chat}
	got, err := processor.Process(context.Background(), input)
	if err != nil {
		t.Fatal(err)
	}
	if !bytes.Equal(got, input) {
		t.Fatalf("success changed bytes:\n%s", got)
	}
	if len(chat.calls) != 0 {
		t.Fatalf("chat calls = %d, want 0", len(chat.calls))
	}
}

func TestProcessorFailureMakesThreeCallsAndOnlyMutatesErrorMessage(t *testing.T) {
	input := failureInput("api_key=supersecret", "fatal: command not found token=abc")
	chat := &fakeChat{responses: []string{`{"error":"command not found"}`, `{"context":"startup"}`, "Main issue: command missing. Recommended fix: install it."}}
	sanitizer, err := logprep.NewSanitizer([]string{`(?i)(api_key|token)=[^\s]+`})
	if err != nil {
		t.Fatal(err)
	}
	processor := testProcessor(chat, sanitizer)
	got, err := processor.Process(context.Background(), input)
	if err != nil {
		t.Fatal(err)
	}
	if len(chat.calls) != 3 {
		t.Fatalf("chat calls = %d, want 3", len(chat.calls))
	}
	first := messagesText(chat.calls[0])
	second := messagesText(chat.calls[1])
	third := messagesText(chat.calls[2])
	if strings.Contains(first+second+third, "supersecret") || strings.Contains(first+second+third, "token=abc") {
		t.Fatal("unredacted secret reached Watson messages")
	}
	if !strings.Contains(first, "command not found") || strings.Contains(first, "startup") {
		t.Fatalf("stderr fresh call was not isolated: %s", first)
	}
	if !strings.Contains(second, "[REDACTED]") || strings.Contains(second, "command not found") {
		t.Fatalf("stdout fresh call was not isolated: %s", second)
	}
	if !strings.Contains(third, "command not found") || !strings.Contains(third, "startup") {
		t.Fatalf("final call lacks prior analyses: %s", third)
	}

	var before, after map[string]any
	if err := json.Unmarshal(input, &before); err != nil {
		t.Fatal(err)
	}
	if err := json.Unmarshal(got, &after); err != nil {
		t.Fatal(err)
	}
	if gotMessage := after["error_message"]; gotMessage != "AI analysis: Main issue: command missing. Recommended fix: install it." {
		t.Fatalf("error_message = %#v", gotMessage)
	}
	delete(before, "error_message")
	delete(after, "error_message")
	if !reflect.DeepEqual(before, after) {
		t.Fatalf("fields other than error_message changed\nbefore=%#v\nafter=%#v", before, after)
	}
}

func TestProcessorChatFailureReturnsExactOriginal(t *testing.T) {
	input := failureInput("stdout", "stderr")
	chat := &fakeChat{responses: []string{"stderr analysis", "stdout analysis", "final"}, failAt: 2}
	got, err := testProcessor(chat, nil).Process(context.Background(), input)
	if err == nil || !strings.Contains(err.Error(), "analyze stdout") {
		t.Fatalf("Process() error = %v", err)
	}
	if !bytes.Equal(got, input) {
		t.Fatalf("fallback changed original bytes: %s", got)
	}
	if len(chat.calls) != 2 {
		t.Fatalf("chat calls = %d, want 2", len(chat.calls))
	}
}

func testProcessor(chat watsonx.ChatClient, sanitizer *logprep.Sanitizer) *Processor {
	return &Processor{
		Config: config.Config{
			Generation: config.GenerationConfig{FreshMaxInputTokens: 1000, FreshMaxOutputTokens: 100, FinalMaxTotalInputTokens: 1000, FinalMaxOutputTokens: 100, TimeLimitMS: 1000},
			HTTP:       config.HTTPConfig{BodyHardLimitBytes: 100_000},
		},
		Prompts: prompts.Loader{
			Root: filepath.Join("..", "..", "config", "ai-status-wrapper", "prompts"), Pipeline: "sync", Version: "v1",
		},
		Chat: chat, Sanitizer: sanitizer,
	}
}

func failureInput(stdout, stderr string) []byte {
	root := map[string]any{
		"success": false, "status": "failed", "exit_code": 127, "wrapper_exit_code": 127,
		"failure_reason": "non_zero_exit_code", "error_message": "original",
		"command": map[string]any{"display": "run command"},
		"summary": map[string]any{"stdout_truncated": false, "stderr_truncated": false},
		"output":  map[string]any{"stdout": stdout, "stderr": stderr},
		"unknown": map[string]any{"nested": true},
	}
	b, _ := json.Marshal(root)
	return b
}

func messagesText(messages []watsonx.Message) string {
	b, _ := json.Marshal(messages)
	return string(b)
}
