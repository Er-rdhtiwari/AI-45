package logprep

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestSanitizer(t *testing.T) {
	s, err := NewSanitizer([]string{`token=[^ ]+`, `(?i)password:\s*\S+`})
	if err != nil {
		t.Fatal(err)
	}
	got := s.Apply("token=abc password: hunter2 safe=value")
	if got != "[REDACTED] [REDACTED] safe=value" {
		t.Fatalf("Apply() = %q", got)
	}
}

func TestSanitizerAlwaysAppliesBaselinePatterns(t *testing.T) {
	s, err := NewSanitizer(nil)
	if err != nil {
		t.Fatal(err)
	}
	got := s.Apply(`{"token": "abc", "password":"hunter,2; still-secret", Authorization: Bearer bearer-secret safe=value}`)
	if strings.Contains(got, "abc") || strings.Contains(got, "still-secret") || strings.Contains(got, "bearer-secret") {
		t.Fatalf("Apply() left a baseline secret unredacted: %q", got)
	}
	if !strings.Contains(got, "safe=value") {
		t.Fatalf("Apply() removed non-secret content: %q", got)
	}
}

func TestPatternsFromFile(t *testing.T) {
	path := filepath.Join(t.TempDir(), "patterns.txt")
	if err := os.WriteFile(path, []byte("# comment\nsecret=.*\n\nkey=.*\n"), 0o600); err != nil {
		t.Fatal(err)
	}
	patterns, err := PatternsFromFile(path)
	if err != nil {
		t.Fatal(err)
	}
	if len(patterns) != 2 {
		t.Fatalf("got %d patterns, want 2", len(patterns))
	}
}

func TestReducePreservesFailureSignalsAndEnd(t *testing.T) {
	input := "start\n" + strings.Repeat("ordinary line with padding\n", 40) + "FATAL: permission denied\n" + strings.Repeat("other line with padding\n", 40) + "last-line"
	got, reduced := Reduce(input, 100, 400)
	if !reduced {
		t.Fatal("Reduce() reduced = false, want true")
	}
	for _, want := range []string{"log reduced", "FATAL: permission denied", "last-line"} {
		if !strings.Contains(got, want) {
			t.Fatalf("Reduce() result missing %q: %q", want, got)
		}
	}
	if len(got) > 400 {
		t.Fatalf("Reduce() length = %d, want <= 400", len(got))
	}
}
