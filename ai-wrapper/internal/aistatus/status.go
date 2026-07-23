package aistatus

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"strconv"
)

type Document struct {
	original        []byte
	root            map[string]any
	success         bool
	status          string
	exitCode        int
	wrapperExitCode int
	stdout          string
	stderr          string
}

func Parse(input []byte) (*Document, error) {
	decoder := json.NewDecoder(bytes.NewReader(input))
	decoder.UseNumber()
	var root map[string]any
	if err := decoder.Decode(&root); err != nil {
		return nil, fmt.Errorf("parse status JSON: %w", err)
	}
	if root == nil {
		return nil, errors.New("parse status JSON: top-level value must be an object")
	}
	var extra any
	if err := decoder.Decode(&extra); !errors.Is(err, io.EOF) {
		if err == nil {
			return nil, errors.New("parse status JSON: multiple JSON values are not allowed")
		}
		return nil, fmt.Errorf("parse status JSON trailing data: %w", err)
	}

	success, err := boolField(root, "success")
	if err != nil {
		return nil, err
	}
	status, err := stringField(root, "status")
	if err != nil {
		return nil, err
	}
	exitCode, err := intField(root, "exit_code")
	if err != nil {
		return nil, err
	}
	wrapperExitCode, err := intField(root, "wrapper_exit_code")
	if err != nil {
		return nil, err
	}

	doc := &Document{
		original:        bytes.Clone(input),
		root:            root,
		success:         success,
		status:          status,
		exitCode:        exitCode,
		wrapperExitCode: wrapperExitCode,
	}
	if !doc.IsSuccessful() {
		output, ok := root["output"].(map[string]any)
		if !ok {
			return nil, errors.New("parse status JSON: field output must be an object for failed status")
		}
		doc.stdout, err = stringField(output, "stdout")
		if err != nil {
			return nil, fmt.Errorf("parse status JSON output: %w", err)
		}
		doc.stderr, err = stringField(output, "stderr")
		if err != nil {
			return nil, fmt.Errorf("parse status JSON output: %w", err)
		}
	}
	return doc, nil
}

func (d *Document) IsSuccessful() bool {
	return d.success && d.status == "success" && d.exitCode == 0 && d.wrapperExitCode == 0
}

func (d *Document) Original() []byte { return bytes.Clone(d.original) }
func (d *Document) Stdout() string   { return d.stdout }
func (d *Document) Stderr() string   { return d.stderr }
func (d *Document) ExitCode() int    { return d.exitCode }

func (d *Document) CommandDisplay() string {
	command, ok := d.root["command"].(map[string]any)
	if !ok {
		return ""
	}
	display, _ := command["display"].(string)
	return display
}

func (d *Document) LogWasTruncated(target string) bool {
	summary, ok := d.root["summary"].(map[string]any)
	if !ok {
		return false
	}
	value, _ := summary[target+"_truncated"].(bool)
	return value
}

func (d *Document) SummaryJSON() (string, error) {
	summary := make(map[string]any)
	for _, key := range []string{
		"success", "status", "exit_code", "wrapper_exit_code", "failure_reason",
		"error_message", "command", "summary", "timed_out", "capture_limit_exceeded",
	} {
		if value, ok := d.root[key]; ok {
			summary[key] = value
		}
	}
	b, err := json.Marshal(summary)
	if err != nil {
		return "", fmt.Errorf("encode status summary: %w", err)
	}
	return string(b), nil
}

func (d *Document) WithErrorMessage(message string) ([]byte, error) {
	d.root["error_message"] = message
	b, err := json.MarshalIndent(d.root, "", "  ")
	if err != nil {
		return nil, fmt.Errorf("encode enriched status JSON: %w", err)
	}
	return b, nil
}

func boolField(root map[string]any, name string) (bool, error) {
	value, ok := root[name]
	if !ok {
		return false, fmt.Errorf("parse status JSON: required field %s is missing", name)
	}
	typed, ok := value.(bool)
	if !ok {
		return false, fmt.Errorf("parse status JSON: field %s must be a boolean", name)
	}
	return typed, nil
}

func stringField(root map[string]any, name string) (string, error) {
	value, ok := root[name]
	if !ok {
		return "", fmt.Errorf("required field %s is missing", name)
	}
	typed, ok := value.(string)
	if !ok {
		return "", fmt.Errorf("field %s must be a string", name)
	}
	return typed, nil
}

func intField(root map[string]any, name string) (int, error) {
	value, ok := root[name]
	if !ok {
		return 0, fmt.Errorf("parse status JSON: required field %s is missing", name)
	}
	number, ok := value.(json.Number)
	if !ok {
		return 0, fmt.Errorf("parse status JSON: field %s must be an integer", name)
	}
	parsed, err := strconv.ParseInt(number.String(), 10, 32)
	if err != nil {
		return 0, fmt.Errorf("parse status JSON: field %s must be an integer", name)
	}
	return int(parsed), nil
}
