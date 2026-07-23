package logprep

import (
	"fmt"
	"strings"
)

const approximateCharactersPerToken = 4

var signalWords = []string{
	"error", "warn", "fail", "exception", "panic", "timeout", "timed out",
	"denied", "not found", "no such file", "fatal", "unauthorized", "forbidden",
}

// Reduce keeps the beginning, failure-signal lines, and end of oversized logs.
// Token counting is intentionally conservative and dependency-free: four UTF-8
// bytes are treated as one token.
func Reduce(input string, maxTokens, maxBytes int) (string, bool) {
	limit := maxTokens * approximateCharactersPerToken
	if maxBytes > 0 && (limit == 0 || maxBytes < limit) {
		limit = maxBytes
	}
	if limit <= 0 || len(input) <= limit {
		return input, false
	}

	lines := strings.Split(input, "\n")
	budget := limit - 160
	if budget < 64 {
		return input[:limit], true
	}
	headBudget := budget * 35 / 100
	tailBudget := budget * 35 / 100
	signalBudget := budget - headBudget - tailBudget

	head := takeFromStart(lines, headBudget)
	tail := takeFromEnd(lines, tailBudget)
	signals := takeSignals(lines, signalBudget)
	reduced := fmt.Sprintf(
		"[log reduced from %d bytes; selected beginning, failure signals, and end]\n%s\n--- failure signal lines ---\n%s\n--- end of log ---\n%s",
		len(input), strings.Join(head, "\n"), strings.Join(signals, "\n"), strings.Join(tail, "\n"),
	)
	if len(reduced) > limit {
		reduced = reduced[:limit]
	}
	return reduced, true
}

func takeFromStart(lines []string, budget int) []string {
	var out []string
	used := 0
	for _, line := range lines {
		if used+len(line)+1 > budget {
			break
		}
		out = append(out, line)
		used += len(line) + 1
	}
	return out
}

func takeFromEnd(lines []string, budget int) []string {
	var reverse []string
	used := 0
	for i := len(lines) - 1; i >= 0; i-- {
		if used+len(lines[i])+1 > budget {
			break
		}
		reverse = append(reverse, lines[i])
		used += len(lines[i]) + 1
	}
	out := make([]string, len(reverse))
	for i := range reverse {
		out[len(reverse)-1-i] = reverse[i]
	}
	return out
}

func takeSignals(lines []string, budget int) []string {
	var out []string
	used := 0
	for _, line := range lines {
		lower := strings.ToLower(line)
		matched := false
		for _, signal := range signalWords {
			if strings.Contains(lower, signal) {
				matched = true
				break
			}
		}
		if !matched {
			continue
		}
		if used+len(line)+1 > budget {
			break
		}
		out = append(out, line)
		used += len(line) + 1
	}
	return out
}
