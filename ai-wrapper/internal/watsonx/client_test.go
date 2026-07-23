package watsonx

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"strings"
	"sync/atomic"
	"testing"
	"time"
)

type staticToken string

func (s staticToken) Token(context.Context) (string, error) { return string(s), nil }

func TestClientSendsChatRequestAndParsesResponse(t *testing.T) {
	server := httptest.NewTLSServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/ml/v1/text/chat" || r.URL.Query().Get("version") != "2024-05-31" {
			t.Errorf("unexpected URL %s", r.URL.String())
		}
		if r.Header.Get("Authorization") != "Bearer token" {
			t.Errorf("Authorization = %q", r.Header.Get("Authorization"))
		}
		var body struct {
			ModelID    string    `json:"model_id"`
			ProjectID  string    `json:"project_id"`
			Messages   []Message `json:"messages"`
			Parameters struct {
				Max int `json:"max_new_tokens"`
			} `json:"parameters"`
		}
		if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
			t.Error(err)
		}
		if body.ModelID != "model" || body.ProjectID != "project" || body.Parameters.Max != 123 || len(body.Messages) != 2 {
			t.Errorf("unexpected request: %#v", body)
		}
		fmt.Fprint(w, `{"choices":[{"message":{"content":" final answer "}}]}`)
	}))
	defer server.Close()

	client := newTestClient(t, server, 0, 0, 10_000)
	got, err := client.Chat(context.Background(), []Message{SystemMessage("system"), UserMessage("user")}, 123, 1000)
	if err != nil || got != "final answer" {
		t.Fatalf("Chat() = %q, %v", got, err)
	}
}

func TestClientRetriesTransientResponse(t *testing.T) {
	var calls atomic.Int32
	server := httptest.NewTLSServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		if calls.Add(1) == 1 {
			w.WriteHeader(http.StatusTooManyRequests)
			return
		}
		fmt.Fprint(w, `{"choices":[{"message":{"content":[{"type":"text","text":"ok"}]}}]}`)
	}))
	defer server.Close()

	client := newTestClient(t, server, 1, time.Millisecond, 10_000)
	got, err := client.Chat(context.Background(), []Message{UserMessage("user")}, 10, 100)
	if err != nil || got != "ok" {
		t.Fatalf("Chat() = %q, %v", got, err)
	}
	if calls.Load() != 2 {
		t.Fatalf("calls = %d, want 2", calls.Load())
	}
}

func TestClientRejectsOversizedBody(t *testing.T) {
	server := httptest.NewTLSServer(http.HandlerFunc(func(http.ResponseWriter, *http.Request) {
		t.Fatal("server should not be called")
	}))
	defer server.Close()
	client := newTestClient(t, server, 0, 0, 100)
	_, err := client.Chat(context.Background(), []Message{UserMessage(strings.Repeat("x", 1000))}, 10, 100)
	if err == nil || !strings.Contains(err.Error(), "exceeding hard limit") {
		t.Fatalf("Chat() error = %v", err)
	}
}

func TestClientRejectsInsecureURL(t *testing.T) {
	_, err := NewClient(ClientOptions{
		BaseURL: "http://watson.example", APIVersion: "2024-05-31", ModelID: "model", ProjectID: "project",
		Tokens: staticToken("token"), HTTPClient: http.DefaultClient, HardBodyLimit: 1000,
	})
	if err == nil || !strings.Contains(err.Error(), "absolute HTTPS URL") {
		t.Fatalf("NewClient() error = %v", err)
	}
}

func TestClientDoesNotFollowRedirects(t *testing.T) {
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

	client := newTestClient(t, source, 0, 0, 10_000)
	_, err := client.Chat(context.Background(), []Message{UserMessage("sensitive log")}, 10, 100)
	if err == nil || !strings.Contains(err.Error(), "HTTP 307") {
		t.Fatalf("Chat() error = %v", err)
	}
	if redirectedCalls.Load() != 0 {
		t.Fatalf("redirect destination received %d calls", redirectedCalls.Load())
	}
}

func newTestClient(t *testing.T, server *httptest.Server, retries int, backoff time.Duration, hardLimit int) *Client {
	t.Helper()
	client, err := NewClient(ClientOptions{
		BaseURL: server.URL, APIVersion: "2024-05-31", ModelID: "model", ProjectID: "project",
		Tokens: staticToken("token"), HTTPClient: server.Client(), Retries: retries, Backoff: backoff, HardBodyLimit: hardLimit,
	})
	if err != nil {
		t.Fatal(err)
	}
	return client
}
