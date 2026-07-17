package watsonx

import (
	"context"
	"fmt"
	"net/http"
	"net/http/httptest"
	"strings"
	"sync/atomic"
	"testing"
	"time"
)

func TestIAMClientGetsAndCachesToken(t *testing.T) {
	var calls atomic.Int32
	server := httptest.NewTLSServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		calls.Add(1)
		if got := r.Header.Get("Content-Type"); !strings.HasPrefix(got, "application/x-www-form-urlencoded") {
			t.Errorf("Content-Type = %q", got)
		}
		if err := r.ParseForm(); err != nil {
			t.Error(err)
		}
		if r.Form.Get("grant_type") != iamGrantType || r.Form.Get("apikey") != "test-key" {
			t.Errorf("unexpected IAM form: %v", r.Form)
		}
		fmt.Fprint(w, `{"access_token":"bearer-token","expires_in":3600}`)
	}))
	defer server.Close()

	client := NewIAMClient(server.URL, "test-key", server.Client(), 0, 0)
	for range 2 {
		token, err := client.Token(context.Background())
		if err != nil || token != "bearer-token" {
			t.Fatalf("Token() = %q, %v", token, err)
		}
	}
	if calls.Load() != 1 {
		t.Fatalf("IAM calls = %d, want 1", calls.Load())
	}
}

func TestIAMClientDoesNotRetryAuthenticationErrors(t *testing.T) {
	var calls atomic.Int32
	server := httptest.NewTLSServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		calls.Add(1)
		w.WriteHeader(http.StatusUnauthorized)
	}))
	defer server.Close()

	client := NewIAMClient(server.URL, "bad-key", server.Client(), 2, time.Millisecond)
	_, err := client.Token(context.Background())
	if err == nil || !strings.Contains(err.Error(), "HTTP 401") {
		t.Fatalf("Token() error = %v", err)
	}
	if calls.Load() != 1 {
		t.Fatalf("IAM calls = %d, want 1", calls.Load())
	}
}

func TestIAMClientRejectsMissingAPIKey(t *testing.T) {
	client := NewIAMClient("https://iam.example", "", http.DefaultClient, 0, 0)
	if _, err := client.Token(context.Background()); err == nil || strings.Contains(err.Error(), "secret") {
		t.Fatalf("Token() error = %v", err)
	}
}

func TestIAMClientRejectsInsecureURL(t *testing.T) {
	client := NewIAMClient("http://iam.example/token", "must-not-be-sent", http.DefaultClient, 0, 0)
	_, err := client.Token(context.Background())
	if err == nil || !strings.Contains(err.Error(), "absolute HTTPS URL") {
		t.Fatalf("Token() error = %v", err)
	}
}

func TestIAMClientDoesNotFollowRedirects(t *testing.T) {
	var redirectedCalls atomic.Int32
	destination := httptest.NewTLSServer(http.HandlerFunc(func(http.ResponseWriter, *http.Request) {
		redirectedCalls.Add(1)
	}))
	defer destination.Close()
	source := httptest.NewTLSServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		w.Header().Set("Location", destination.URL)
		w.WriteHeader(http.StatusTemporaryRedirect)
	}))
	defer source.Close()

	client := NewIAMClient(source.URL, "must-not-be-sent", source.Client(), 0, 0)
	_, err := client.Token(context.Background())
	if err == nil || !strings.Contains(err.Error(), "HTTP 307") {
		t.Fatalf("Token() error = %v", err)
	}
	if redirectedCalls.Load() != 0 {
		t.Fatalf("redirect destination received %d calls", redirectedCalls.Load())
	}
}

func TestIAMClientRejectsOversizedResponse(t *testing.T) {
	server := httptest.NewTLSServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		fmt.Fprint(w, `{"access_token":"token","expires_in":3600}`)
		fmt.Fprint(w, strings.Repeat(" ", iamResponseLimitBytes))
	}))
	defer server.Close()

	client := NewIAMClient(server.URL, "test-key", server.Client(), 0, 0)
	_, err := client.Token(context.Background())
	if err == nil || !strings.Contains(err.Error(), "exceeds hard limit") {
		t.Fatalf("Token() error = %v", err)
	}
}
