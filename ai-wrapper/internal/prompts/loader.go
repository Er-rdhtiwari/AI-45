package prompts

import (
	"errors"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"sort"
	"strings"
)

const maxPromptFileBytes = 1024 * 1024

type Loader struct {
	Root                string
	Pipeline            string
	Version             string
	AllowCommonFallback bool
	EnableFewShot       bool
	MaxExamples         int
}

type Pack struct {
	System    string
	User      string
	Assistant string
	Examples  []string
}

// Load resolves a deterministic prompt path such as
// sync/v1/stderr/fresh.system.md. System and user are required; assistant is
// optional.
func (l Loader) Load(target, call string) (Pack, error) {
	if err := validateSegment("pipeline", l.Pipeline); err != nil {
		return Pack{}, err
	}
	if err := validateSegment("version", l.Version); err != nil {
		return Pack{}, err
	}
	if err := validateSegment("target", target); err != nil {
		return Pack{}, err
	}
	if err := validateSegment("call", call); err != nil {
		return Pack{}, err
	}

	pack, err := l.loadFrom(filepath.Join(l.Root, l.Pipeline, l.Version), target, call)
	if err != nil && l.AllowCommonFallback {
		pack, err = l.loadFrom(filepath.Join(l.Root, "common"), target, call)
	}
	if err != nil {
		return Pack{}, err
	}
	if l.EnableFewShot && l.MaxExamples > 0 {
		pack.Examples, err = loadExamples(l.Root, filepath.Join(l.Root, l.Pipeline, l.Version, "examples"), l.MaxExamples)
		if err != nil {
			return Pack{}, err
		}
	}
	return pack, nil
}

func (l Loader) loadFrom(base, target, call string) (Pack, error) {
	readRequired := func(role string) (string, error) {
		path := filepath.Join(base, target, call+"."+role+".md")
		b, err := readPromptFile(l.Root, path)
		if err != nil {
			return "", fmt.Errorf("load required %s prompt %q: %w", role, path, err)
		}
		if strings.TrimSpace(string(b)) == "" {
			return "", fmt.Errorf("load required %s prompt %q: file is empty", role, path)
		}
		return string(b), nil
	}

	system, err := readRequired("system")
	if err != nil {
		return Pack{}, err
	}
	user, err := readRequired("user")
	if err != nil {
		return Pack{}, err
	}
	assistantPath := filepath.Join(base, target, call+".assistant.md")
	assistant, err := readPromptFile(l.Root, assistantPath)
	if err != nil && !errors.Is(err, os.ErrNotExist) {
		return Pack{}, fmt.Errorf("load optional assistant prompt %q: %w", assistantPath, err)
	}
	return Pack{System: system, User: user, Assistant: string(assistant)}, nil
}

func loadExamples(root, dir string, limit int) ([]string, error) {
	resolvedDir, err := resolveWithinRoot(root, dir)
	if errors.Is(err, os.ErrNotExist) {
		return nil, nil
	}
	if err != nil {
		return nil, fmt.Errorf("load prompt examples: %w", err)
	}
	info, err := os.Stat(resolvedDir)
	if err != nil {
		return nil, fmt.Errorf("load prompt examples: %w", err)
	}
	if !info.IsDir() {
		return nil, errors.New("load prompt examples: examples path is not a directory")
	}
	entries, err := os.ReadDir(resolvedDir)
	if err != nil {
		return nil, fmt.Errorf("load prompt examples: %w", err)
	}
	names := make([]string, 0, len(entries))
	for _, entry := range entries {
		if !entry.IsDir() && strings.HasSuffix(entry.Name(), ".md") {
			names = append(names, entry.Name())
		}
	}
	sort.Strings(names)
	if len(names) > limit {
		names = names[:limit]
	}
	examples := make([]string, 0, len(names))
	for _, name := range names {
		b, err := readPromptFile(root, filepath.Join(resolvedDir, name))
		if err != nil {
			return nil, fmt.Errorf("load prompt example %q: %w", name, err)
		}
		if strings.TrimSpace(string(b)) != "" {
			examples = append(examples, string(b))
		}
	}
	return examples, nil
}

func readPromptFile(root, path string) ([]byte, error) {
	resolved, err := resolveWithinRoot(root, path)
	if err != nil {
		return nil, err
	}
	info, err := os.Stat(resolved)
	if err != nil {
		return nil, err
	}
	if !info.Mode().IsRegular() {
		return nil, errors.New("prompt path is not a regular file")
	}
	file, err := os.Open(resolved)
	if err != nil {
		return nil, err
	}
	defer file.Close()
	content, err := io.ReadAll(io.LimitReader(file, maxPromptFileBytes+1))
	if err != nil {
		return nil, err
	}
	if len(content) > maxPromptFileBytes {
		return nil, fmt.Errorf("prompt file exceeds %d-byte limit", maxPromptFileBytes)
	}
	return content, nil
}

func resolveWithinRoot(root, path string) (string, error) {
	resolvedRoot, err := filepath.EvalSymlinks(root)
	if err != nil {
		return "", err
	}
	resolvedPath, err := filepath.EvalSymlinks(path)
	if err != nil {
		return "", err
	}
	resolvedRoot, err = filepath.Abs(resolvedRoot)
	if err != nil {
		return "", err
	}
	resolvedPath, err = filepath.Abs(resolvedPath)
	if err != nil {
		return "", err
	}
	relative, err := filepath.Rel(resolvedRoot, resolvedPath)
	if err != nil {
		return "", err
	}
	if relative == ".." || strings.HasPrefix(relative, ".."+string(filepath.Separator)) {
		return "", errors.New("prompt path resolves outside prompt root")
	}
	return resolvedPath, nil
}

func validateSegment(name, value string) error {
	if value == "" || value == "." || value == ".." || strings.ContainsAny(value, `/\\`) {
		return fmt.Errorf("invalid prompt %s %q", name, value)
	}
	return nil
}
