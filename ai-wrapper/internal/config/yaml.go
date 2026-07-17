package config

import (
	"bufio"
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"strconv"
	"strings"
	"unicode"
)

// This parser intentionally supports only the small, safe YAML subset used by
// the wrapper configuration: indentation-based maps, lists, quoted/plain
// scalars, booleans, null, and numbers. Keeping the accepted grammar narrow
// avoids a third-party dependency and rejects aliases, tags, merge keys, and
// multi-document configuration.

type yamlLine struct {
	number  int
	indent  int
	content string
}

func parseYAML(data []byte) (map[string]any, error) {
	lines, err := tokenizeYAML(data)
	if err != nil {
		return nil, err
	}
	if len(lines) == 0 {
		return nil, errors.New("configuration is empty")
	}
	if lines[0].indent != 0 {
		return nil, fmt.Errorf("line %d: top-level mapping must start at indentation 0", lines[0].number)
	}
	value, next, err := parseYAMLBlock(lines, 0, 0)
	if err != nil {
		return nil, err
	}
	if next != len(lines) {
		return nil, fmt.Errorf("line %d: unexpected content", lines[next].number)
	}
	root, ok := value.(map[string]any)
	if !ok {
		return nil, errors.New("top-level configuration must be a mapping")
	}
	return root, nil
}

func tokenizeYAML(data []byte) ([]yamlLine, error) {
	scanner := bufio.NewScanner(bytes.NewReader(data))
	scanner.Buffer(make([]byte, 4096), 1024*1024)
	var lines []yamlLine
	lineNumber := 0
	for scanner.Scan() {
		lineNumber++
		line := strings.TrimSuffix(scanner.Text(), "\r")
		indent := 0
		for indent < len(line) {
			switch line[indent] {
			case ' ':
				indent++
			case '\t':
				return nil, fmt.Errorf("line %d: tabs are not allowed for indentation", lineNumber)
			default:
				goto indentationDone
			}
		}
	indentationDone:
		content := strings.TrimSpace(stripYAMLComment(line[indent:]))
		if content == "" {
			continue
		}
		if content == "---" || content == "..." {
			return nil, fmt.Errorf("line %d: YAML document markers are not supported", lineNumber)
		}
		lines = append(lines, yamlLine{number: lineNumber, indent: indent, content: content})
	}
	if err := scanner.Err(); err != nil {
		return nil, fmt.Errorf("read configuration: %w", err)
	}
	return lines, nil
}

func parseYAMLBlock(lines []yamlLine, index, indent int) (any, int, error) {
	if index >= len(lines) {
		return nil, index, errors.New("unexpected end of configuration")
	}
	if lines[index].indent != indent {
		return nil, index, fmt.Errorf("line %d: inconsistent indentation", lines[index].number)
	}
	if isYAMLSequenceItem(lines[index].content) {
		return parseYAMLSequence(lines, index, indent)
	}
	return parseYAMLMap(lines, index, indent)
}

func parseYAMLMap(lines []yamlLine, index, indent int) (map[string]any, int, error) {
	result := make(map[string]any)
	for index < len(lines) {
		line := lines[index]
		if line.indent < indent {
			break
		}
		if line.indent > indent {
			return nil, index, fmt.Errorf("line %d: unexpected indentation", line.number)
		}
		if isYAMLSequenceItem(line.content) {
			return nil, index, fmt.Errorf("line %d: cannot mix mapping and sequence entries at the same indentation", line.number)
		}
		key, rawValue, ok := splitYAMLMapping(line.content)
		if !ok {
			return nil, index, fmt.Errorf("line %d: expected key: value", line.number)
		}
		if err := validateYAMLKey(key); err != nil {
			return nil, index, fmt.Errorf("line %d: %w", line.number, err)
		}
		if _, exists := result[key]; exists {
			return nil, index, fmt.Errorf("line %d: duplicate key %q", line.number, key)
		}
		index++
		if rawValue != "" {
			value, err := parseYAMLScalar(rawValue)
			if err != nil {
				return nil, index, fmt.Errorf("line %d: value for %q: %w", line.number, key, err)
			}
			result[key] = value
			continue
		}
		if index >= len(lines) || lines[index].indent <= indent {
			return nil, index, fmt.Errorf("line %d: key %q requires a nested value", line.number, key)
		}
		value, next, err := parseYAMLBlock(lines, index, lines[index].indent)
		if err != nil {
			return nil, index, err
		}
		result[key] = value
		index = next
	}
	return result, index, nil
}

func parseYAMLSequence(lines []yamlLine, index, indent int) ([]any, int, error) {
	var result []any
	for index < len(lines) {
		line := lines[index]
		if line.indent < indent {
			break
		}
		if line.indent > indent {
			return nil, index, fmt.Errorf("line %d: unexpected indentation in sequence", line.number)
		}
		if !isYAMLSequenceItem(line.content) {
			return nil, index, fmt.Errorf("line %d: cannot mix sequence and mapping entries at the same indentation", line.number)
		}
		rest := strings.TrimSpace(strings.TrimPrefix(line.content, "-"))
		index++
		if rest == "" {
			if index >= len(lines) || lines[index].indent <= indent {
				return nil, index, fmt.Errorf("line %d: sequence item requires a nested value", line.number)
			}
			value, next, err := parseYAMLBlock(lines, index, lines[index].indent)
			if err != nil {
				return nil, index, err
			}
			result = append(result, value)
			index = next
			continue
		}

		key, rawValue, mappingItem := splitYAMLMapping(rest)
		if !mappingItem {
			value, err := parseYAMLScalar(rest)
			if err != nil {
				return nil, index, fmt.Errorf("line %d: sequence value: %w", line.number, err)
			}
			if index < len(lines) && lines[index].indent > indent {
				return nil, index, fmt.Errorf("line %d: scalar sequence item cannot have nested content", lines[index].number)
			}
			result = append(result, value)
			continue
		}

		if err := validateYAMLKey(key); err != nil {
			return nil, index, fmt.Errorf("line %d: %w", line.number, err)
		}
		item := make(map[string]any)
		if rawValue != "" {
			value, err := parseYAMLScalar(rawValue)
			if err != nil {
				return nil, index, fmt.Errorf("line %d: value for %q: %w", line.number, key, err)
			}
			item[key] = value
		} else {
			itemIndent := indent + 2
			if index >= len(lines) || lines[index].indent <= itemIndent {
				return nil, index, fmt.Errorf("line %d: key %q requires a nested value", line.number, key)
			}
			value, next, err := parseYAMLBlock(lines, index, lines[index].indent)
			if err != nil {
				return nil, index, err
			}
			item[key] = value
			index = next
		}

		if index < len(lines) && lines[index].indent > indent {
			continuationIndent := lines[index].indent
			continuation, next, err := parseYAMLMap(lines, index, continuationIndent)
			if err != nil {
				return nil, index, err
			}
			for continuationKey, value := range continuation {
				if _, duplicate := item[continuationKey]; duplicate {
					return nil, index, fmt.Errorf("line %d: duplicate key %q", lines[index].number, continuationKey)
				}
				item[continuationKey] = value
			}
			index = next
		}
		result = append(result, item)
	}
	return result, index, nil
}

func parseYAMLScalar(raw string) (any, error) {
	raw = strings.TrimSpace(raw)
	if raw == "" {
		return nil, errors.New("empty scalar")
	}
	if strings.HasPrefix(raw, `"`) {
		value, err := strconv.Unquote(raw)
		if err != nil {
			return nil, fmt.Errorf("invalid double-quoted string: %w", err)
		}
		return value, nil
	}
	if strings.HasPrefix(raw, "'") {
		if len(raw) < 2 || !strings.HasSuffix(raw, "'") {
			return nil, errors.New("unterminated single-quoted string")
		}
		return strings.ReplaceAll(raw[1:len(raw)-1], "''", "'"), nil
	}
	switch strings.ToLower(raw) {
	case "true":
		return true, nil
	case "false":
		return false, nil
	case "null", "~":
		return nil, nil
	}
	if integer, err := strconv.ParseInt(raw, 10, 64); err == nil {
		return integer, nil
	}
	if number, err := strconv.ParseFloat(raw, 64); err == nil {
		return number, nil
	}
	if strings.HasPrefix(raw, "[") || strings.HasPrefix(raw, "{") {
		var value any
		if err := json.Unmarshal([]byte(raw), &value); err != nil {
			return nil, fmt.Errorf("invalid inline JSON value: %w", err)
		}
		return value, nil
	}
	if strings.HasPrefix(raw, "&") || strings.HasPrefix(raw, "*") || strings.HasPrefix(raw, "!") || strings.HasPrefix(raw, "|") || strings.HasPrefix(raw, ">") {
		return nil, errors.New("YAML anchors, aliases, tags, and block scalars are not supported")
	}
	return raw, nil
}

func splitYAMLMapping(content string) (key, value string, ok bool) {
	singleQuoted := false
	doubleQuoted := false
	escaped := false
	for index := 0; index < len(content); index++ {
		character := content[index]
		if doubleQuoted {
			if escaped {
				escaped = false
				continue
			}
			if character == '\\' {
				escaped = true
				continue
			}
			if character == '"' {
				doubleQuoted = false
			}
			continue
		}
		if singleQuoted {
			if character == '\'' {
				if index+1 < len(content) && content[index+1] == '\'' {
					index++
					continue
				}
				singleQuoted = false
			}
			continue
		}
		switch character {
		case '"':
			doubleQuoted = true
		case '\'':
			singleQuoted = true
		case ':':
			key = strings.TrimSpace(content[:index])
			value = strings.TrimSpace(content[index+1:])
			return key, value, key != ""
		}
	}
	return "", "", false
}

func stripYAMLComment(content string) string {
	singleQuoted := false
	doubleQuoted := false
	escaped := false
	for index := 0; index < len(content); index++ {
		character := content[index]
		if doubleQuoted {
			if escaped {
				escaped = false
				continue
			}
			if character == '\\' {
				escaped = true
				continue
			}
			if character == '"' {
				doubleQuoted = false
			}
			continue
		}
		if singleQuoted {
			if character == '\'' {
				if index+1 < len(content) && content[index+1] == '\'' {
					index++
					continue
				}
				singleQuoted = false
			}
			continue
		}
		switch character {
		case '"':
			doubleQuoted = true
		case '\'':
			singleQuoted = true
		case '#':
			if index == 0 || unicode.IsSpace(rune(content[index-1])) {
				return content[:index]
			}
		}
	}
	return content
}

func isYAMLSequenceItem(content string) bool {
	return content == "-" || strings.HasPrefix(content, "- ")
}

func validateYAMLKey(key string) error {
	if key == "" {
		return errors.New("mapping key must not be empty")
	}
	for _, character := range key {
		if !(unicode.IsLetter(character) || unicode.IsDigit(character) || character == '_' || character == '-') {
			return fmt.Errorf("unsupported mapping key %q", key)
		}
	}
	return nil
}
