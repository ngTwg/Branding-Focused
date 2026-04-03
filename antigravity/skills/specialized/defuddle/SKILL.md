---
name: "defuddle"
tags: ["antigravity", "c:", "data-engineering", "defuddle", "formats", "gemini", "<YOUR_USERNAME>", "output", "specialized", "usage", "use", "users", "when"]
tier: 3
risk: "high"
estimated_tokens: 342
tools_needed: ["git", "markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["data", "analytics"]
quality_score: 0.67
date_added: "2026-03-21"
description: "Extract clean markdown content from web pages using Defuddle CLI, removing clutter and navigation to save tokens. Use instead of WebFetch when the user provides a URL to read or analyze, for online documentation, articles, blog posts, or any standard web page."
source: "https://github.com/kepano/obsidian-skills"
---
# Defuddle

Use Defuddle CLI to extract clean readable content from web pages. Prefer over WebFetch for standard web pages — it removes navigation, ads, and clutter, reducing token usage.

## When to Use

- Use when the user provides a normal webpage URL to read, summarize, or analyze.
- Prefer it over noisy page-fetch approaches when token efficiency matters.
- Use for docs, articles, blog posts, and similar public web content.

If not installed: `npm install -g defuddle`

## Usage

Always use `--md` for markdown output:

```bash
defuddle parse <url> --md
```

Save to file:

```bash
defuddle parse <url> --md -o content.md
```

Extract specific metadata:

```bash
defuddle parse <url> -p title
defuddle parse <url> -p description
defuddle parse <url> -p domain
```

## Output formats

| Flag | Format |
|------|--------|
| `--md` | Markdown (default choice) |
| `--json` | JSON with both HTML and markdown |
| (none) | HTML |
| `-p <name>` | Specific metadata property |
