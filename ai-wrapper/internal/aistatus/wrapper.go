package aistatus

import (
	"context"
	"fmt"
	"strings"

	"ai-status-wrapper/internal/config"
	"ai-status-wrapper/internal/logprep"
	"ai-status-wrapper/internal/prompts"
	"ai-status-wrapper/internal/watsonx"
)

type Processor struct {
	Config    config.Config
	Prompts   prompts.Loader
	Chat      watsonx.ChatClient
	Sanitizer *logprep.Sanitizer
}

// Process is the safe library entrypoint. Any parsing or enrichment error is
// returned alongside the exact original bytes so callers can preserve the
// existing pipeline result.
func (p *Processor) Process(ctx context.Context, input []byte) ([]byte, error) {
	doc, err := Parse(input)
	if err != nil {
		return input, err
	}
	if doc.IsSuccessful() {
		return doc.Original(), nil
	}
	return p.Enrich(ctx, doc)
}

func (p *Processor) Enrich(ctx context.Context, doc *Document) ([]byte, error) {
	if p.Chat == nil {
		return doc.Original(), fmt.Errorf("enrich status: Watson chat client is required")
	}
	stderr, stderrReduced := p.prepareLog(doc.Stderr())
	stdout, stdoutReduced := p.prepareLog(doc.Stdout())

	stderrAnalysis, err := p.analyzeFresh(ctx, doc, "stderr", stderr, stderrReduced || doc.LogWasTruncated("stderr"))
	if err != nil {
		return doc.Original(), fmt.Errorf("analyze stderr: %w", err)
	}
	stdoutAnalysis, err := p.analyzeFresh(ctx, doc, "stdout", stdout, stdoutReduced || doc.LogWasTruncated("stdout"))
	if err != nil {
		return doc.Original(), fmt.Errorf("analyze stdout: %w", err)
	}
	finalMessage, err := p.analyzeFinal(ctx, doc, stderrAnalysis, stdoutAnalysis)
	if err != nil {
		return doc.Original(), fmt.Errorf("produce final analysis: %w", err)
	}
	finalMessage = strings.TrimSpace(finalMessage)
	if finalMessage == "" {
		return doc.Original(), fmt.Errorf("produce final analysis: Watson returned an empty message")
	}
	if !strings.HasPrefix(strings.ToLower(finalMessage), "ai analysis:") {
		finalMessage = "AI analysis: " + finalMessage
	}
	enriched, err := doc.WithErrorMessage(finalMessage)
	if err != nil {
		return doc.Original(), err
	}
	return enriched, nil
}

func (p *Processor) analyzeFresh(ctx context.Context, doc *Document, target, log string, truncated bool) (string, error) {
	pack, err := p.Prompts.Load(target, "fresh")
	if err != nil {
		return "", err
	}
	note := "The available log was not truncated."
	if truncated {
		note = "The available log was truncated or reduced. Analyze only the supplied content."
	}
	values := map[string]string{
		"command":         p.sanitize(doc.CommandDisplay()),
		"exit_code":       fmt.Sprintf("%d", doc.ExitCode()),
		"stdout":          "",
		"stderr":          "",
		"truncation_note": note,
	}
	values[target] = log
	messages, err := buildMessages(pack, values)
	if err != nil {
		return "", err
	}
	return p.Chat.Chat(ctx, messages, p.Config.Generation.FreshMaxOutputTokens, p.Config.Generation.TimeLimitMS)
}

func (p *Processor) analyzeFinal(ctx context.Context, doc *Document, stderrAnalysis, stdoutAnalysis string) (string, error) {
	pack, err := p.Prompts.Load("final", "context")
	if err != nil {
		return "", err
	}
	statusSummary, err := doc.SummaryJSON()
	if err != nil {
		return "", err
	}
	analysisBudget := p.Config.Generation.FinalMaxTotalInputTokens / 3
	stderrAnalysis, _ = logprep.Reduce(stderrAnalysis, analysisBudget, p.Config.HTTP.BodyHardLimitBytes/3)
	stdoutAnalysis, _ = logprep.Reduce(stdoutAnalysis, analysisBudget, p.Config.HTTP.BodyHardLimitBytes/3)
	values := map[string]string{
		"status_summary":  p.sanitize(statusSummary),
		"stderr_analysis": p.sanitize(stderrAnalysis),
		"stdout_analysis": p.sanitize(stdoutAnalysis),
		"command":         p.sanitize(doc.CommandDisplay()),
		"exit_code":       fmt.Sprintf("%d", doc.ExitCode()),
	}
	messages, err := buildMessages(pack, values)
	if err != nil {
		return "", err
	}
	return p.Chat.Chat(ctx, messages, p.Config.Generation.FinalMaxOutputTokens, p.Config.Generation.TimeLimitMS)
}

func (p *Processor) prepareLog(log string) (string, bool) {
	log = p.sanitize(log)
	return logprep.Reduce(log, p.Config.Generation.FreshMaxInputTokens, p.Config.HTTP.BodyHardLimitBytes/3)
}

func (p *Processor) sanitize(value string) string {
	if p.Sanitizer == nil {
		return value
	}
	return p.Sanitizer.Apply(value)
}

func buildMessages(pack prompts.Pack, values map[string]string) ([]watsonx.Message, error) {
	system, err := prompts.Render(pack.System, values)
	if err != nil {
		return nil, err
	}
	user, err := prompts.Render(pack.User, values)
	if err != nil {
		return nil, err
	}
	messages := []watsonx.Message{watsonx.SystemMessage(system)}

	var references []string
	for _, example := range pack.Examples {
		rendered, err := prompts.Render(example, values)
		if err != nil {
			return nil, err
		}
		references = append(references, rendered)
	}
	if strings.TrimSpace(pack.Assistant) != "" {
		assistant, err := prompts.Render(pack.Assistant, values)
		if err != nil {
			return nil, err
		}
		referenceText := "Use the following response pattern."
		if len(references) > 0 {
			referenceText += "\n\nReference examples:\n" + strings.Join(references, "\n\n---\n\n")
		}
		messages = append(messages, watsonx.UserMessage(referenceText), watsonx.AssistantMessage(assistant))
	} else if len(references) > 0 {
		user = "Reference examples:\n" + strings.Join(references, "\n\n---\n\n") + "\n\nCurrent failure:\n" + user
	}
	messages = append(messages, watsonx.UserMessage(user))
	return messages, nil
}
