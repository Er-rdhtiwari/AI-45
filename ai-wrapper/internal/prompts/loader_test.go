package prompts

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestLoaderLoadsRequiredOptionalAndSortedExamples(t *testing.T) {
	root := t.TempDir()
	base := filepath.Join(root, "sync", "v1")
	mustWrite(t, filepath.Join(base, "stderr", "fresh.system.md"), "system {{command}}")
	mustWrite(t, filepath.Join(base, "stderr", "fresh.user.md"), "user {{stderr}}")
	mustWrite(t, filepath.Join(base, "stderr", "fresh.assistant.md"), "shape")
	mustWrite(t, filepath.Join(base, "examples", "b.md"), "second")
	mustWrite(t, filepath.Join(base, "examples", "a.md"), "first")

	pack, err := (Loader{Root: root, Pipeline: "sync", Version: "v1", EnableFewShot: true, MaxExamples: 1}).Load("stderr", "fresh")
	if err != nil {
		t.Fatalf("Load() error = %v", err)
	}
	if pack.Assistant != "shape" || len(pack.Examples) != 1 || pack.Examples[0] != "first" {
		t.Fatalf("unexpected pack: %#v", pack)
	}
}

func TestLoaderRequiresSystemAndUser(t *testing.T) {
	root := t.TempDir()
	base := filepath.Join(root, "sync", "v1", "stdout")
	mustWrite(t, filepath.Join(base, "fresh.system.md"), "system")
	_, err := (Loader{Root: root, Pipeline: "sync", Version: "v1"}).Load("stdout", "fresh")
	if err == nil || !strings.Contains(err.Error(), "required user") {
		t.Fatalf("Load() error = %v, want missing-user error", err)
	}
}

func TestLoaderRejectsPathTraversal(t *testing.T) {
	_, err := (Loader{Root: t.TempDir(), Pipeline: "../sync", Version: "v1"}).Load("stderr", "fresh")
	if err == nil || !strings.Contains(err.Error(), "invalid prompt pipeline") {
		t.Fatalf("Load() error = %v, want path-validation error", err)
	}
}

func TestLoaderRejectsSymlinkOutsidePromptRoot(t *testing.T) {
	root := t.TempDir()
	base := filepath.Join(root, "sync", "v1", "stderr")
	mustWrite(t, filepath.Join(base, "fresh.user.md"), "user")
	outside := filepath.Join(t.TempDir(), "secret")
	mustWrite(t, outside, "must not be loaded")
	if err := os.Symlink(outside, filepath.Join(base, "fresh.system.md")); err != nil {
		t.Skipf("cannot create symlink: %v", err)
	}

	_, err := (Loader{Root: root, Pipeline: "sync", Version: "v1"}).Load("stderr", "fresh")
	if err == nil || !strings.Contains(err.Error(), "outside prompt root") {
		t.Fatalf("Load() error = %v, want prompt-root confinement error", err)
	}
}

func TestRender(t *testing.T) {
	got, err := Render("command={{ command }}, code={{exit_code}}", map[string]string{"command": "go test", "exit_code": "1"})
	if err != nil {
		t.Fatal(err)
	}
	if got != "command=go test, code=1" {
		t.Fatalf("Render() = %q", got)
	}
	if _, err := Render("{{missing}}", nil); err == nil {
		t.Fatal("Render() expected a missing-value error")
	}
}

func mustWrite(t *testing.T, path, content string) {
	t.Helper()
	if err := os.MkdirAll(filepath.Dir(path), 0o755); err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(path, []byte(content), 0o600); err != nil {
		t.Fatal(err)
	}
}
