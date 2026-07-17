package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"reflect"
	"regexp"
	"strconv"
	"strings"
	"testing"
)

const (
	realE2EEnvironment      = "RUN_WATSONX_E2E"
	realE2EMinScoreVariable = "WATSONX_E2E_MIN_SCORE"
	realE2EFixtureVariable  = "WATSONX_E2E_FIXTURE"
)

type e2eScore struct {
	Preservation  int
	MessageChange int
	Evidence      int
	Actionability int
	Reliability   int
	Total         int
}

func TestRealWatsonEndToEndScore(t *testing.T) {
	if os.Getenv(realE2EEnvironment) != "1" {
		t.Skip("set RUN_WATSONX_E2E=1 to make real IAM and Watson API calls")
	}

	fixtureDirectory := filepath.Join("..", "..", "testdata", "status")
	fixtureNames, err := realE2EFixtureNames(fixtureDirectory, os.Getenv(realE2EFixtureVariable))
	if err != nil {
		t.Fatal(err)
	}
	if includesFailureFixture(fixtureNames) {
		for _, name := range []string{"WATSONX_API_KEY", "WATSONX_PROJECT_ID"} {
			if strings.TrimSpace(os.Getenv(name)) == "" {
				t.Fatalf("%s is required when the real end-to-end test includes failure fixtures", name)
			}
		}
	}
	minimum := e2eMinimumScore(t)
	t.Logf("Watson E2E fixtures: %s", strings.Join(fixtureNames, ", "))
	for _, fixtureName := range fixtureNames {
		t.Run(strings.TrimSuffix(fixtureName, filepath.Ext(fixtureName)), func(t *testing.T) {
			fixturePath := filepath.Join(fixtureDirectory, fixtureName)
			input, err := os.ReadFile(fixturePath)
			if err != nil {
				t.Fatalf("read E2E fixture %q: %v", fixtureName, err)
			}
			before := decodeE2EObject(t, input)
			var stdout, stderr bytes.Buffer
			exit := run([]string{
				"--config", filepath.Join("..", "..", "config", "ai-status-wrapper", "config.yaml"),
				"--prompts", filepath.Join("..", "..", "config", "ai-status-wrapper", "prompts"),
				"--pipeline", "sync",
				"--prompt-version", "v1",
				"--timeout", "2m",
				"--log-level", "info",
			}, bytes.NewReader(input), &stdout, &stderr)
			if exit != 0 {
				t.Fatalf("wrapper exit = %d: %s", exit, stderr.String())
			}
			if e2eObjectIsSuccessful(before) {
				if !bytes.Equal(stdout.Bytes(), input) {
					t.Fatalf("successful fixture was not preserved byte-for-byte\nwant: %s\n got: %s", input, stdout.Bytes())
				}
				t.Log("successful input preserved byte-for-byte; Watson enrichment skipped")
				return
			}

			after := decodeE2EObject(t, stdout.Bytes())
			score := scoreE2EOutput(before, after)
			message, _ := after["error_message"].(string)
			t.Logf("Watson E2E score: %d/100 (preservation=%d/40, message=%d/20, evidence=%d/20, actionability=%d/10, reliability=%d/10)",
				score.Total, score.Preservation, score.MessageChange, score.Evidence, score.Actionability, score.Reliability)
			t.Logf("Watson error_message: %s", message)

			if score.Preservation != 40 {
				t.Fatalf("Watson output changed fields other than error_message; score=%d/100", score.Total)
			}
			if issues := reliabilityIssues(before, message); len(issues) > 0 {
				t.Fatalf("Watson output contains unreliable guidance: %s; score=%d/100", strings.Join(issues, "; "), score.Total)
			}
			if score.Total < minimum {
				t.Fatalf("Watson E2E score %d is below required minimum %d; wrapper diagnostics: %s",
					score.Total, minimum, stderr.String())
			}
		})
	}
}

func TestRealE2EFixtureNames(t *testing.T) {
	directory := filepath.Join("..", "..", "testdata", "status")
	wantAll := []string{
		"failure-invalid-kubernetes-yaml.json",
		"failure-permission-denied.json",
		"failure-rollout-timeout.json",
		"failure.json",
		"success.json",
	}
	got, err := realE2EFixtureNames(directory, "")
	if err != nil {
		t.Fatal(err)
	}
	if !reflect.DeepEqual(got, wantAll) {
		t.Fatalf("default fixtures = %q, want %q", got, wantAll)
	}
	got, err = realE2EFixtureNames(directory, " failure-rollout-timeout.json ")
	if err != nil {
		t.Fatal(err)
	}
	if !reflect.DeepEqual(got, []string{"failure-rollout-timeout.json"}) {
		t.Fatalf("selected fixtures = %q", got)
	}
	got, err = realE2EFixtureNames(directory, " success.json ")
	if err != nil {
		t.Fatal(err)
	}
	if !reflect.DeepEqual(got, []string{"success.json"}) {
		t.Fatalf("selected success fixture = %q", got)
	}
	for _, selected := range []string{"notes.txt", "../failure.json", "failure-missing.json"} {
		if _, err := realE2EFixtureNames(directory, selected); err == nil {
			t.Fatalf("selection %q should fail", selected)
		}
	}
}

func realE2EFixtureNames(directory, selected string) ([]string, error) {
	selected = strings.TrimSpace(selected)
	if selected != "" {
		matchesJSONName, err := filepath.Match("*.json", selected)
		if err != nil || filepath.Base(selected) != selected || !matchesJSONName {
			return nil, fmt.Errorf("%s must be a JSON file name from testdata/status, got %q", realE2EFixtureVariable, selected)
		}
		info, err := os.Stat(filepath.Join(directory, selected))
		if err != nil {
			return nil, fmt.Errorf("read E2E fixture %q: %w", selected, err)
		}
		if !info.Mode().IsRegular() {
			return nil, fmt.Errorf("E2E fixture %q is not a regular file", selected)
		}
		return []string{selected}, nil
	}

	paths, err := filepath.Glob(filepath.Join(directory, "*.json"))
	if err != nil {
		return nil, fmt.Errorf("discover E2E fixtures: %w", err)
	}
	if len(paths) == 0 {
		return nil, fmt.Errorf("no JSON E2E fixtures found in %s", directory)
	}
	names := make([]string, 0, len(paths))
	for _, path := range paths {
		names = append(names, filepath.Base(path))
	}
	return names, nil
}

func includesFailureFixture(names []string) bool {
	for _, name := range names {
		if strings.HasPrefix(name, "failure") {
			return true
		}
	}
	return false
}

func e2eObjectIsSuccessful(status map[string]any) bool {
	success, _ := status["success"].(bool)
	statusName, _ := status["status"].(string)
	exitCode, exitOK := status["exit_code"].(json.Number)
	wrapperExitCode, wrapperExitOK := status["wrapper_exit_code"].(json.Number)
	return success && statusName == "success" && exitOK && exitCode.String() == "0" &&
		wrapperExitOK && wrapperExitCode.String() == "0"
}

func TestScoreE2EOutput(t *testing.T) {
	input, err := os.ReadFile(filepath.Join("..", "..", "testdata", "status", "failure.json"))
	if err != nil {
		t.Fatal(err)
	}
	before := decodeE2EObject(t, input)
	after := decodeE2EObject(t, input)
	after["error_message"] = "AI analysis: Main issue: The profile comparison failed because yq was not found. Evidence: stderr reports yq: command not found and exit code 127. Most likely root cause: the step image lacks Mike Farah yq v4 on PATH. Recommended fix: rebuild the image with a pinned yq v4 binary for its OS and architecture and verify its checksum. Follow-up checks: run yq --version in that image, then rerun the pipeline."
	score := scoreE2EOutput(before, after)
	if score.Total != 100 {
		t.Fatalf("score = %+v, want 100/100 for a complete evidence-based response", score)
	}
}

func TestScoreE2EOutputRejectsUnreliableGuidance(t *testing.T) {
	input, err := os.ReadFile(filepath.Join("..", "..", "testdata", "status", "failure.json"))
	if err != nil {
		t.Fatal(err)
	}
	before := decodeE2EObject(t, input)
	tests := []struct {
		name    string
		message string
		issue   string
	}{
		{
			name:    "ambiguous distro package",
			message: "AI analysis: Main issue: yq is missing. Evidence: yq: command not found. Recommended fix: apt-get update && apt-get install -y yq. Follow-up checks: verify yq.",
			issue:   "distro package",
		},
		{
			name:    "isolated pre-step filesystem",
			message: "AI analysis: Main issue: yq is missing. Evidence: yq: command not found. Recommended fix: add a Tekton pre-step that writes yq to /usr/local/bin. Follow-up checks: rerun.",
			issue:   "shared workspace",
		},
		{
			name:    "unsupported go speculation",
			message: "AI analysis: Main issue: yq is missing. Evidence: yq: command not found. Recommended fix: install yq. Follow-up checks: confirm the go toolchain is present because go may also be missing.",
			issue:   "unsupported go",
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			after := decodeE2EObject(t, input)
			after["error_message"] = tt.message
			score := scoreE2EOutput(before, after)
			if score.Reliability != 0 {
				t.Fatalf("reliability = %d, want 0", score.Reliability)
			}
			issues := reliabilityIssues(before, tt.message)
			if !strings.Contains(strings.Join(issues, " "), tt.issue) {
				t.Fatalf("issues = %q, want an issue containing %q", issues, tt.issue)
			}
		})
	}
}

func TestReliabilityIssuesRecognizesAdditionalScenarios(t *testing.T) {
	tests := []struct {
		name        string
		file        string
		goodMessage string
		badMessage  string
		badIssue    string
	}{
		{
			name:        "permission denied",
			file:        "failure-permission-denied.json",
			goodMessage: "AI analysis: The deploy script lacks execute permission. Evidence: stderr says Permission denied and reports that the script is not executable. Fix the executable file mode in source or the image and rerun.",
			badMessage:  "AI analysis: The deployment failed because the cluster is unavailable. Verify the cluster and rerun.",
			badIssue:    "execute-permission",
		},
		{
			name:        "rollout timeout",
			file:        "failure-rollout-timeout.json",
			goodMessage: "AI analysis: The Kubernetes rollout timed out because an old onboarding-api replica remained pending termination. Inspect the old pod, resolve its termination blocker, and rerun rollout status.",
			badMessage:  "AI analysis: The deployment manifest is invalid. Fix its fields and rerun kubectl.",
			badIssue:    "rollout-timeout",
		},
		{
			name:        "invalid kubernetes yaml",
			file:        "failure-invalid-kubernetes-yaml.json",
			goodMessage: "AI analysis: Server-side validation rejected the unknown Deployment field replica. Rename it to replicas in config/deployment.yaml, validate again, and rerun kubectl apply.",
			badMessage:  "AI analysis: Kubernetes credentials are unavailable. Configure credentials and rerun.",
			badIssue:    "invalid-field",
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			input, err := os.ReadFile(filepath.Join("..", "..", "testdata", "status", tt.file))
			if err != nil {
				t.Fatal(err)
			}
			status := decodeE2EObject(t, input)
			if issues := reliabilityIssues(status, tt.goodMessage); len(issues) != 0 {
				t.Fatalf("good guidance rejected: %q", issues)
			}
			issues := reliabilityIssues(status, tt.badMessage)
			if !strings.Contains(strings.Join(issues, " "), tt.badIssue) {
				t.Fatalf("issues = %q, want an issue containing %q", issues, tt.badIssue)
			}
		})
	}
}

func scoreE2EOutput(before, after map[string]any) e2eScore {
	var score e2eScore
	beforeComparable := copyWithoutErrorMessage(before)
	afterComparable := copyWithoutErrorMessage(after)
	if reflect.DeepEqual(beforeComparable, afterComparable) {
		score.Preservation = 40
	}

	originalMessage, _ := before["error_message"].(string)
	message, _ := after["error_message"].(string)
	message = strings.TrimSpace(message)
	if message != "" && message != strings.TrimSpace(originalMessage) {
		score.MessageChange += 10
	}
	if strings.HasPrefix(strings.ToLower(message), "ai analysis:") {
		score.MessageChange += 10
	}

	evidence := statusEvidence(before)
	evidenceTokens := meaningfulTokens(evidence)
	messageTokens := meaningfulTokens(message)
	overlap := 0
	for token := range messageTokens {
		if _, ok := evidenceTokens[token]; ok {
			overlap++
		}
	}
	score.Evidence = minInt(20, overlap*5)

	actionTerms := []string{
		"add", "configure", "dependency", "ensure", "fix", "image", "install",
		"path", "provide", "rebuild", "rerun", "update", "verify",
	}
	actionMatches := 0
	for _, term := range actionTerms {
		if _, ok := messageTokens[term]; ok {
			actionMatches++
		}
	}
	score.Actionability = minInt(10, actionMatches*5)
	if len(reliabilityIssues(before, message)) == 0 {
		score.Reliability = 10
	}
	score.Total = score.Preservation + score.MessageChange + score.Evidence + score.Actionability + score.Reliability
	return score
}

var aptYQPattern = regexp.MustCompile(`(?i)\bapt(?:-get)?\b[^\n]{0,80}\binstall\b[^\n]{0,80}\byq\b`)

func reliabilityIssues(status map[string]any, message string) []string {
	normalized := strings.ToLower(strings.TrimSpace(message))
	var issues []string
	if aptYQPattern.MatchString(normalized) {
		issues = append(issues, "unqualified distro package may not provide Mike Farah yq v4")
	}
	mentionsPreStep := strings.Contains(normalized, "pre-step") || strings.Contains(normalized, "prestep")
	mentionsSharedStorage := strings.Contains(normalized, "shared workspace") ||
		strings.Contains(normalized, "shared volume") || strings.Contains(normalized, "workspace mounted")
	if mentionsPreStep && !mentionsSharedStorage {
		issues = append(issues, "Tekton pre-step advice must use a shared workspace or volume")
	}
	goSpeculation := strings.Contains(normalized, "go toolchain") || strings.Contains(normalized, "missing go") ||
		strings.Contains(normalized, "go may also be missing") || strings.Contains(normalized, "go executable")
	evidence := strings.ToLower(statusEvidence(status))
	if strings.Contains(evidence, "yq: command not found") &&
		(!strings.Contains(normalized, "yq") ||
			!(strings.Contains(normalized, "not found") || strings.Contains(normalized, "unavailable") || strings.Contains(normalized, "missing") || strings.Contains(normalized, "lacks"))) {
		issues = append(issues, "missing-yq evidence was not diagnosed")
	}
	if strings.Contains(evidence, "permission denied") &&
		(!strings.Contains(normalized, "permission") ||
			!(strings.Contains(normalized, "executable") || strings.Contains(normalized, "execute") || strings.Contains(normalized, "chmod") || strings.Contains(normalized, "file mode"))) {
		issues = append(issues, "execute-permission evidence was not diagnosed")
	}
	if strings.Contains(evidence, "timed out waiting for the condition") &&
		(!(strings.Contains(normalized, "timed out") || strings.Contains(normalized, "timeout")) ||
			!strings.Contains(normalized, "rollout")) {
		issues = append(issues, "rollout-timeout evidence was not diagnosed")
	}
	if strings.Contains(evidence, `unknown field "replica"`) &&
		(!strings.Contains(normalized, "replica") ||
			!(strings.Contains(normalized, "unknown field") || strings.Contains(normalized, "replicas") || strings.Contains(normalized, "validation"))) {
		issues = append(issues, "invalid-field evidence was not diagnosed")
	}
	directGoFailure := strings.Contains(evidence, "go: command not found") ||
		strings.Contains(evidence, `required executable "go"`) || strings.Contains(evidence, "go executable is unavailable")
	if goSpeculation && !directGoFailure {
		issues = append(issues, "unsupported go failure speculation")
	}
	if len(strings.Fields(message)) > 180 {
		issues = append(issues, "response exceeds the 180-word pipeline-log limit")
	}
	return issues
}

func statusEvidence(status map[string]any) string {
	var parts []string
	if output, ok := status["output"].(map[string]any); ok {
		for _, name := range []string{"stderr", "stdout"} {
			if value, ok := output[name].(string); ok {
				parts = append(parts, value)
			}
		}
	}
	if command, ok := status["command"].(map[string]any); ok {
		if display, ok := command["display"].(string); ok {
			parts = append(parts, display)
		}
	}
	return strings.Join(parts, "\n")
}

var e2eTokenPattern = regexp.MustCompile(`[[:alnum:]][[:alnum:]_./-]*`)

func meaningfulTokens(value string) map[string]struct{} {
	stopWords := map[string]struct{}{
		"and": {}, "are": {}, "because": {}, "before": {}, "for": {}, "from": {},
		"has": {}, "into": {}, "not": {}, "that": {}, "the": {}, "this": {}, "was": {},
		"with": {},
	}
	tokens := make(map[string]struct{})
	for _, token := range e2eTokenPattern.FindAllString(strings.ToLower(value), -1) {
		if len(token) < 3 {
			continue
		}
		if _, stopped := stopWords[token]; stopped {
			continue
		}
		tokens[token] = struct{}{}
	}
	return tokens
}

func copyWithoutErrorMessage(source map[string]any) map[string]any {
	copy := make(map[string]any, len(source))
	for key, value := range source {
		if key != "error_message" {
			copy[key] = value
		}
	}
	return copy
}

func decodeE2EObject(t *testing.T, input []byte) map[string]any {
	t.Helper()
	decoder := json.NewDecoder(bytes.NewReader(input))
	decoder.UseNumber()
	var object map[string]any
	if err := decoder.Decode(&object); err != nil {
		t.Fatalf("decode E2E status: %v\n%s", err, input)
	}
	return object
}

func e2eMinimumScore(t *testing.T) int {
	t.Helper()
	raw := strings.TrimSpace(os.Getenv(realE2EMinScoreVariable))
	if raw == "" {
		return 70
	}
	value, err := strconv.Atoi(raw)
	if err != nil || value < 0 || value > 100 {
		t.Fatalf("%s must be an integer from 0 to 100, got %q", realE2EMinScoreVariable, raw)
	}
	return value
}

func minInt(left, right int) int {
	if left < right {
		return left
	}
	return right
}
