package config

import (
	"reflect"
	"strings"
	"testing"
)

func TestParseYAMLSupportedSubset(t *testing.T) {
	input := []byte(`
# leading comment
name: "value # retained"
single: 'it''s valid'
plain: value#part # removed comment
enabled: true
count: 2
nothing: null
nested:
  item: child
models:
  - id: "model/one"
    limit: 100
  - id: "model/two"
    limit: 200
patterns:
  - '(?i)token\s*=\s*\S+'
  - "literal"
`)
	got, err := parseYAML(input)
	if err != nil {
		t.Fatalf("parseYAML() error = %v", err)
	}
	want := map[string]any{
		"name": "value # retained", "single": "it's valid", "plain": "value#part",
		"enabled": true, "count": int64(2), "nothing": nil,
		"nested": map[string]any{"item": "child"},
		"models": []any{
			map[string]any{"id": "model/one", "limit": int64(100)},
			map[string]any{"id": "model/two", "limit": int64(200)},
		},
		"patterns": []any{`(?i)token\s*=\s*\S+`, "literal"},
	}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("parseYAML()\ngot:  %#v\nwant: %#v", got, want)
	}
}

func TestParseYAMLRejectsUnsupportedOrAmbiguousInput(t *testing.T) {
	tests := map[string]string{
		"document marker": "---\nkey: value\n",
		"duplicate key":   "key: one\nkey: two\n",
		"tab indentation": "root:\n\tkey: value\n",
		"anchor":          "key: &shared value\n",
		"mixed block":     "root:\n  - one\n  key: value\n",
	}
	for name, input := range tests {
		t.Run(name, func(t *testing.T) {
			if _, err := parseYAML([]byte(input)); err == nil {
				t.Fatalf("parseYAML(%q) expected an error", input)
			}
		})
	}
}

func TestLoadShippedConfigRequiresRuntimeProjectID(t *testing.T) {
	_, err := Load("../../config/ai-status-wrapper/config.yaml")
	if err == nil || !strings.Contains(err.Error(), "watsonx.project_id is required") {
		t.Fatalf("Load() error = %v, want required project ID after successful YAML parsing", err)
	}
}
