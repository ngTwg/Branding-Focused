---
name: "Claude API — Ruby"
tags: ["anthropic_api_key", "antigravity", "api", "basic", "c:", "claude", "client", "default", "env", "explicit", "frontend", "gemini", "initialization", "installation", "key", "<YOUR_USERNAME>", "message", "request", "ruby", "specialized"]
tier: 2
risk: "medium"
estimated_tokens: 453
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.80
---
# Claude API — Ruby

> **Note:** The Ruby SDK supports the Claude API. A tool runner is available in beta via `client.beta.messages.tool_runner()`. Agent SDK is not yet available for Ruby.

## Installation

```bash
gem install anthropic
```

## Client Initialization

```ruby
require "anthropic"

# Default (uses ANTHROPIC_API_KEY env var)
client = Anthropic::Client.new

# Explicit API key
client = Anthropic::Client.new(api_key: "your-api-key")
```

---

## Basic Message Request

```ruby
message = client.messages.create(
  model: :"claude-opus-4-6",
  max_tokens: 1024,
  messages: [
    { role: "user", content: "What is the capital of France?" }
  ]
)
puts message.content.first.text
```

---

## Streaming

```ruby
stream = client.messages.stream(
  model: :"claude-opus-4-6",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Write a haiku" }]
)

stream.text.each { |text| print(text) }
```

---

## Tool Use

The Ruby SDK supports tool use via raw JSON schema definitions and also provides a beta tool runner for automatic tool execution.

### Tool Runner (Beta)

```ruby
class GetWeatherInput < Anthropic::BaseModel
  required :location, String, doc: "City and state, e.g. San Francisco, CA"
end

class GetWeather < Anthropic::BaseTool
  doc "Get the current weather for a location"

  input_schema GetWeatherInput

  def call(input)
    "The weather in #{input.location} is sunny and 72°F."
  end
end

client.beta.messages.tool_runner(
  model: :"claude-opus-4-6",
  max_tokens: 1024,
  tools: [GetWeather.new],
  messages: [{ role: "user", content: "What's the weather in San Francisco?" }]
).each_message do |message|
  puts message.content
end
```

### Manual Loop

See the [shared tool use concepts](../shared/tool-use-concepts.md) for the tool definition format and agentic loop pattern.
