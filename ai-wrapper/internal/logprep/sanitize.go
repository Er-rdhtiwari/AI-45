package logprep

import (
	"bufio"
	"errors"
	"fmt"
	"os"
	"regexp"
	"strings"
)

type Sanitizer struct {
	patterns []*regexp.Regexp
}

var baselineRedactionPatterns = []string{
	`(?i)\b(api[_-]?key|access[_-]?token|auth[_-]?token|token|password|passwd|secret)["']?[[:space:]]*[:=][[:space:]]*["'][^"'\r\n]+["']`,
	`(?i)\b(api[_-]?key|access[_-]?token|auth[_-]?token|token|password|passwd|secret)["']?[[:space:]]*[:=][[:space:]]*["']?[^[:space:],;}"']+`,
	`(?i)\bauthorization[[:space:]]*:[[:space:]]*bearer[[:space:]]+[^[:space:]]+`,
}

func NewSanitizer(patterns []string) (*Sanitizer, error) {
	s := &Sanitizer{}
	for _, pattern := range baselineRedactionPatterns {
		re, err := regexp.Compile(pattern)
		if err != nil {
			return nil, errors.New("compile baseline redaction pattern: invalid regular expression")
		}
		s.patterns = append(s.patterns, re)
	}
	for i, pattern := range patterns {
		pattern = strings.TrimSpace(pattern)
		if pattern == "" || strings.HasPrefix(pattern, "#") {
			continue
		}
		re, err := regexp.Compile(pattern)
		if err != nil {
			return nil, fmt.Errorf("compile redaction pattern %d: invalid regular expression", i+1)
		}
		s.patterns = append(s.patterns, re)
	}
	return s, nil
}

func PatternsFromFile(path string) ([]string, error) {
	if path == "" {
		return nil, nil
	}
	f, err := os.Open(path)
	if err != nil {
		return nil, fmt.Errorf("open redaction pattern file: %w", err)
	}
	defer f.Close()

	var patterns []string
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line != "" && !strings.HasPrefix(line, "#") {
			patterns = append(patterns, line)
		}
	}
	if err := scanner.Err(); err != nil {
		return nil, fmt.Errorf("read redaction pattern file: %w", err)
	}
	return patterns, nil
}

func (s *Sanitizer) Apply(input string) string {
	if s == nil {
		return input
	}
	for _, re := range s.patterns {
		input = re.ReplaceAllString(input, "[REDACTED]")
	}
	return input
}
