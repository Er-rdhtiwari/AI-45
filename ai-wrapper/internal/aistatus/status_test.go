package aistatus

import (
	"bytes"
	"context"
	"encoding/json"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestParseClassifiesOnlyExactSuccess(t *testing.T) {
	success := []byte(`{"success":true,"status":"success","exit_code":0,"wrapper_exit_code":0}`)
	doc, err := Parse(success)
	if err != nil {
		t.Fatal(err)
	}
	if !doc.IsSuccessful() || !bytes.Equal(doc.Original(), success) {
		t.Fatal("expected exact successful pass-through document")
	}

	failure := []byte(`{"success":true,"status":"success","exit_code":1,"wrapper_exit_code":0,"output":{"stdout":"","stderr":"failed"}}`)
	doc, err = Parse(failure)
	if err != nil {
		t.Fatal(err)
	}
	if doc.IsSuccessful() {
		t.Fatal("one mismatched field must classify as failure")
	}
}

func TestParseRejectsInvalidOrIncompleteInput(t *testing.T) {
	for _, input := range []string{
		`not-json`,
		`{"success":false,"status":"failed","exit_code":1}`,
		`{"success":false,"status":"failed","exit_code":1,"wrapper_exit_code":1}`,
		`{"success":false,"status":"failed","exit_code":1,"wrapper_exit_code":1,"output":{"stdout":"x"}}`,
	} {
		if _, err := Parse([]byte(input)); err == nil {
			t.Fatalf("Parse(%q) expected an error", input)
		}
	}
}

func TestProcessParseFailureReturnsOriginal(t *testing.T) {
	input := []byte("not-json\n")
	got, err := (&Processor{}).Process(context.Background(), input)
	if err == nil || !strings.Contains(err.Error(), "parse status JSON") {
		t.Fatalf("Process() error = %v", err)
	}
	if !bytes.Equal(got, input) {
		t.Fatalf("Process() changed fallback bytes: %q", got)
	}
}

func TestFailureEndToEndFixturesAreConsistent(t *testing.T) {
	tests := []struct {
		name           string
		file           string
		exitCode       int
		timedOut       bool
		stdoutEvidence string
		stderrEvidence string
	}{
		{name: "missing yq", file: "failure.json", exitCode: 127, stdoutEvidence: "normalizing YAML", stderrEvidence: "yq: command not found"},
		{name: "permission denied", file: "failure-permission-denied.json", exitCode: 126, stderrEvidence: "Permission denied"},
		{name: "rollout timeout", file: "failure-rollout-timeout.json", exitCode: 124, timedOut: true, stdoutEvidence: "pending termination", stderrEvidence: "timed out waiting"},
		{name: "invalid kubernetes yaml", file: "failure-invalid-kubernetes-yaml.json", exitCode: 1, stderrEvidence: `unknown field "replica"`},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			fixturePath := filepath.Join("..", "..", "testdata", "status", tt.file)
			input, err := os.ReadFile(fixturePath)
			if err != nil {
				t.Fatal(err)
			}
			doc, err := Parse(input)
			if err != nil {
				t.Fatal(err)
			}
			if doc.IsSuccessful() || !strings.Contains(doc.Stdout(), tt.stdoutEvidence) ||
				!strings.Contains(doc.Stderr(), tt.stderrEvidence) {
				t.Fatalf("fixture %s does not contain the expected failure evidence", tt.file)
			}

			var fixture struct {
				Success         bool   `json:"success"`
				Status          string `json:"status"`
				ExitCode        int    `json:"exit_code"`
				WrapperExitCode int    `json:"wrapper_exit_code"`
				FailureReason   string `json:"failure_reason"`
				TimedOut        bool   `json:"timed_out"`
				ErrorMessage    string `json:"error_message"`
				Command         struct {
					Display string `json:"display"`
				} `json:"command"`
				Summary struct {
					TotalLogLines int    `json:"total_log_lines"`
					StdoutLines   int    `json:"stdout_lines"`
					StderrLines   int    `json:"stderr_lines"`
					FirstError    string `json:"first_error"`
					StdoutBytes   int    `json:"stdout_raw_bytes"`
					StderrBytes   int    `json:"stderr_raw_bytes"`
				} `json:"summary"`
				Output struct {
					Stdout string `json:"stdout"`
					Stderr string `json:"stderr"`
				} `json:"output"`
			}
			if err := json.Unmarshal(input, &fixture); err != nil {
				t.Fatal(err)
			}
			if fixture.Success || fixture.Status != "failed" || fixture.ExitCode != tt.exitCode ||
				fixture.WrapperExitCode != tt.exitCode || fixture.TimedOut != tt.timedOut ||
				fixture.FailureReason == "" || fixture.ErrorMessage == "" || fixture.Command.Display == "" {
				t.Fatalf("fixture %s has inconsistent failure metadata", tt.file)
			}
			if fixture.Summary.StdoutBytes != len(fixture.Output.Stdout) ||
				fixture.Summary.StderrBytes != len(fixture.Output.Stderr) ||
				fixture.Summary.StdoutLines != strings.Count(fixture.Output.Stdout, "\n") ||
				fixture.Summary.StderrLines != strings.Count(fixture.Output.Stderr, "\n") ||
				fixture.Summary.TotalLogLines != fixture.Summary.StdoutLines+fixture.Summary.StderrLines ||
				!strings.Contains(fixture.Output.Stderr, fixture.Summary.FirstError) {
				t.Fatalf("fixture %s summary does not match its output content", tt.file)
			}
		})
	}
}
