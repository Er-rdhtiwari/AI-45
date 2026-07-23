package watsonx

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"strings"
	"time"
)

type Message struct {
	Role    string `json:"role"`
	Content any    `json:"content"`
}

type TextContent struct {
	Type string `json:"type"`
	Text string `json:"text"`
}

func SystemMessage(text string) Message {
	return Message{Role: "system", Content: text}
}

func UserMessage(text string) Message {
	return Message{Role: "user", Content: []TextContent{{Type: "text", Text: text}}}
}

func AssistantMessage(text string) Message {
	return Message{Role: "assistant", Content: text}
}

type ChatClient interface {
	Chat(ctx context.Context, messages []Message, maxOutputTokens, timeLimitMS int) (string, error)
}

type Client struct {
	baseURL       string
	apiVersion    string
	modelID       string
	projectID     string
	tokens        TokenProvider
	httpClient    *http.Client
	retries       int
	backoff       time.Duration
	hardBodyLimit int
}

type ClientOptions struct {
	BaseURL       string
	APIVersion    string
	ModelID       string
	ProjectID     string
	Tokens        TokenProvider
	HTTPClient    *http.Client
	Retries       int
	Backoff       time.Duration
	HardBodyLimit int
}

func NewClient(options ClientOptions) (*Client, error) {
	if options.Tokens == nil || options.HTTPClient == nil {
		return nil, errors.New("create Watson client: token provider and HTTP client are required")
	}
	if strings.TrimSpace(options.BaseURL) == "" || strings.TrimSpace(options.APIVersion) == "" ||
		strings.TrimSpace(options.ModelID) == "" || strings.TrimSpace(options.ProjectID) == "" {
		return nil, errors.New("create Watson client: URL, API version, model ID, and project ID are required")
	}
	if options.HardBodyLimit <= 0 {
		return nil, errors.New("create Watson client: hard body limit must be positive")
	}
	baseURL, err := validateHTTPSURL(options.BaseURL, "Watson URL")
	if err != nil {
		return nil, fmt.Errorf("create Watson client: %w", err)
	}
	return &Client{
		baseURL:       strings.TrimRight(baseURL, "/"),
		apiVersion:    options.APIVersion,
		modelID:       options.ModelID,
		projectID:     options.ProjectID,
		tokens:        options.Tokens,
		httpClient:    withoutRedirects(options.HTTPClient),
		retries:       options.Retries,
		backoff:       options.Backoff,
		hardBodyLimit: options.HardBodyLimit,
	}, nil
}

func validateHTTPSURL(rawURL, name string) (string, error) {
	parsed, err := url.Parse(strings.TrimSpace(rawURL))
	if err != nil {
		return "", fmt.Errorf("%s is invalid", name)
	}
	if !strings.EqualFold(parsed.Scheme, "https") || parsed.Host == "" || parsed.Hostname() == "" || parsed.Opaque != "" {
		return "", fmt.Errorf("%s must be an absolute HTTPS URL", name)
	}
	if parsed.User != nil {
		return "", fmt.Errorf("%s must not contain user information", name)
	}
	if parsed.RawQuery != "" || parsed.Fragment != "" {
		return "", fmt.Errorf("%s must not contain a query or fragment", name)
	}
	return parsed.String(), nil
}

func withoutRedirects(client *http.Client) *http.Client {
	if client == nil {
		return nil
	}
	clone := *client
	clone.CheckRedirect = func(*http.Request, []*http.Request) error {
		return http.ErrUseLastResponse
	}
	return &clone
}

func (c *Client) Chat(ctx context.Context, messages []Message, maxOutputTokens, timeLimitMS int) (string, error) {
	token, err := c.tokens.Token(ctx)
	if err != nil {
		return "", err
	}
	payload := struct {
		Messages   []Message `json:"messages"`
		Parameters struct {
			MaxNewTokens int `json:"max_new_tokens"`
			TimeLimit    int `json:"time_limit"`
		} `json:"parameters"`
		ModelID   string `json:"model_id"`
		ProjectID string `json:"project_id"`
	}{Messages: messages, ModelID: c.modelID, ProjectID: c.projectID}
	payload.Parameters.MaxNewTokens = maxOutputTokens
	payload.Parameters.TimeLimit = timeLimitMS
	body, err := json.Marshal(payload)
	if err != nil {
		return "", fmt.Errorf("encode Watson chat request: %w", err)
	}
	if len(body) > c.hardBodyLimit {
		return "", fmt.Errorf("Watson chat request body is %d bytes, exceeding hard limit %d", len(body), c.hardBodyLimit)
	}
	endpoint, err := c.endpoint()
	if err != nil {
		return "", err
	}

	var lastErr error
	for attempt := 0; attempt <= c.retries; attempt++ {
		if attempt > 0 {
			if err := waitForRetry(ctx, c.backoff, attempt); err != nil {
				return "", err
			}
		}
		req, err := http.NewRequestWithContext(ctx, http.MethodPost, endpoint, bytes.NewReader(body))
		if err != nil {
			return "", fmt.Errorf("create Watson chat request: %w", err)
		}
		req.Header.Set("Authorization", "Bearer "+token)
		req.Header.Set("Content-Type", "application/json")
		resp, err := c.httpClient.Do(req)
		if err != nil {
			lastErr = fmt.Errorf("Watson chat request failed: %w", err)
			continue
		}
		responseBody, readErr := io.ReadAll(io.LimitReader(resp.Body, int64(c.hardBodyLimit)+1))
		resp.Body.Close()
		if readErr != nil {
			lastErr = fmt.Errorf("read Watson chat response: %w", readErr)
			continue
		}
		if len(responseBody) > c.hardBodyLimit {
			return "", fmt.Errorf("Watson chat response exceeds hard limit %d", c.hardBodyLimit)
		}
		if resp.StatusCode < 200 || resp.StatusCode >= 300 {
			lastErr = fmt.Errorf("Watson chat request returned HTTP %d", resp.StatusCode)
			if !isRetryable(resp.StatusCode) {
				return "", lastErr
			}
			continue
		}
		content, err := parseChatResponse(responseBody)
		if err != nil {
			return "", err
		}
		return content, nil
	}
	return "", lastErr
}

func (c *Client) endpoint() (string, error) {
	endpoint, err := url.Parse(c.baseURL + "/ml/v1/text/chat")
	if err != nil {
		return "", fmt.Errorf("parse Watson URL: %w", err)
	}
	query := endpoint.Query()
	query.Set("version", c.apiVersion)
	endpoint.RawQuery = query.Encode()
	return endpoint.String(), nil
}

func parseChatResponse(body []byte) (string, error) {
	var payload struct {
		Choices []struct {
			Message struct {
				Content json.RawMessage `json:"content"`
			} `json:"message"`
		} `json:"choices"`
		Results []struct {
			GeneratedText string `json:"generated_text"`
		} `json:"results"`
	}
	if err := json.Unmarshal(body, &payload); err != nil {
		return "", fmt.Errorf("decode Watson chat response: %w", err)
	}
	if len(payload.Choices) > 0 {
		content, err := parseContent(payload.Choices[0].Message.Content)
		if err != nil {
			return "", err
		}
		if strings.TrimSpace(content) != "" {
			return strings.TrimSpace(content), nil
		}
	}
	if len(payload.Results) > 0 && strings.TrimSpace(payload.Results[0].GeneratedText) != "" {
		return strings.TrimSpace(payload.Results[0].GeneratedText), nil
	}
	return "", errors.New("Watson chat response did not contain message content")
}

func parseContent(raw json.RawMessage) (string, error) {
	var text string
	if err := json.Unmarshal(raw, &text); err == nil {
		return text, nil
	}
	var blocks []struct {
		Type string `json:"type"`
		Text string `json:"text"`
	}
	if err := json.Unmarshal(raw, &blocks); err != nil {
		return "", errors.New("Watson chat response content has an unsupported shape")
	}
	parts := make([]string, 0, len(blocks))
	for _, block := range blocks {
		if block.Text != "" {
			parts = append(parts, block.Text)
		}
	}
	return strings.Join(parts, "\n"), nil
}
