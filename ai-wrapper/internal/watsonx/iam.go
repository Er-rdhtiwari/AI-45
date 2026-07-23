package watsonx

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"strings"
	"sync"
	"time"
)

const iamGrantType = "urn:ibm:params:oauth:grant-type:apikey"

const iamResponseLimitBytes = 1024 * 1024

type TokenProvider interface {
	Token(context.Context) (string, error)
}

type IAMClient struct {
	endpoint    string
	endpointErr error
	apiKey      string
	httpClient  *http.Client
	retries     int
	backoff     time.Duration

	mu        sync.Mutex
	token     string
	expiresAt time.Time
}

func NewIAMClient(endpoint, apiKey string, httpClient *http.Client, retries int, backoff time.Duration) *IAMClient {
	validatedEndpoint, endpointErr := validateHTTPSURL(endpoint, "IAM token URL")
	return &IAMClient{
		endpoint:    validatedEndpoint,
		endpointErr: endpointErr,
		apiKey:      apiKey,
		httpClient:  withoutRedirects(httpClient),
		retries:     retries,
		backoff:     backoff,
	}
}

func (c *IAMClient) Token(ctx context.Context) (string, error) {
	c.mu.Lock()
	defer c.mu.Unlock()
	if c.endpointErr != nil {
		return "", c.endpointErr
	}
	if c.httpClient == nil {
		return "", errors.New("IAM HTTP client is missing")
	}
	if c.token != "" && time.Now().Add(30*time.Second).Before(c.expiresAt) {
		return c.token, nil
	}
	if strings.TrimSpace(c.apiKey) == "" {
		return "", errors.New("IAM API key is missing")
	}

	form := url.Values{
		"grant_type": []string{iamGrantType},
		"apikey":     []string{c.apiKey},
	}.Encode()
	var lastErr error
	for attempt := 0; attempt <= c.retries; attempt++ {
		if attempt > 0 {
			if err := waitForRetry(ctx, c.backoff, attempt); err != nil {
				return "", err
			}
		}
		req, err := http.NewRequestWithContext(ctx, http.MethodPost, c.endpoint, strings.NewReader(form))
		if err != nil {
			return "", fmt.Errorf("create IAM token request: %w", err)
		}
		req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
		resp, err := c.httpClient.Do(req)
		if err != nil {
			lastErr = fmt.Errorf("IAM token request failed: %w", err)
			continue
		}
		body, readErr := io.ReadAll(io.LimitReader(resp.Body, iamResponseLimitBytes+1))
		resp.Body.Close()
		if readErr != nil {
			lastErr = fmt.Errorf("read IAM token response: %w", readErr)
			continue
		}
		if len(body) > iamResponseLimitBytes {
			return "", fmt.Errorf("IAM token response exceeds hard limit %d", iamResponseLimitBytes)
		}
		if resp.StatusCode < 200 || resp.StatusCode >= 300 {
			lastErr = fmt.Errorf("IAM token request returned HTTP %d", resp.StatusCode)
			if !isRetryable(resp.StatusCode) {
				return "", lastErr
			}
			continue
		}
		var payload struct {
			AccessToken string `json:"access_token"`
			ExpiresIn   int64  `json:"expires_in"`
			Expiration  int64  `json:"expiration"`
		}
		if err := json.Unmarshal(body, &payload); err != nil {
			return "", fmt.Errorf("decode IAM token response: %w", err)
		}
		if payload.AccessToken == "" {
			return "", errors.New("IAM token response did not contain access_token")
		}
		expiresAt := time.Now().Add(time.Duration(payload.ExpiresIn) * time.Second)
		if payload.Expiration > 0 {
			expiresAt = time.Unix(payload.Expiration, 0)
		}
		if payload.ExpiresIn == 0 && payload.Expiration == 0 {
			expiresAt = time.Now().Add(5 * time.Minute)
		}
		c.token = payload.AccessToken
		c.expiresAt = expiresAt
		return c.token, nil
	}
	return "", lastErr
}

func isRetryable(status int) bool {
	return status == http.StatusTooManyRequests || status >= 500
}

func waitForRetry(ctx context.Context, base time.Duration, attempt int) error {
	if base <= 0 {
		return nil
	}
	delay := base * time.Duration(1<<(attempt-1))
	timer := time.NewTimer(delay)
	defer timer.Stop()
	select {
	case <-ctx.Done():
		return ctx.Err()
	case <-timer.C:
		return nil
	}
}
