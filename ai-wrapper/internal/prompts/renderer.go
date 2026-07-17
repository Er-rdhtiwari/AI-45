package prompts

import (
	"fmt"
	"regexp"
	"sort"
	"strings"
)

var placeholderPattern = regexp.MustCompile(`\{\{\s*([a-zA-Z0-9_]+)\s*\}\}`)

func Render(template string, values map[string]string) (string, error) {
	missing := make(map[string]struct{})
	rendered := placeholderPattern.ReplaceAllStringFunc(template, func(match string) string {
		parts := placeholderPattern.FindStringSubmatch(match)
		value, ok := values[parts[1]]
		if !ok {
			missing[parts[1]] = struct{}{}
			return match
		}
		return value
	})
	if len(missing) > 0 {
		names := make([]string, 0, len(missing))
		for name := range missing {
			names = append(names, name)
		}
		sort.Strings(names)
		return "", fmt.Errorf("render prompt: missing values for %s", strings.Join(names, ", "))
	}
	return rendered, nil
}
