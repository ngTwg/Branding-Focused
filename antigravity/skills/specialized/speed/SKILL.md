---
name: "speed"
tags: ["antigravity", "arguments", "c:", "data-engineering", "gemini", "instructions", "<YOUR_USERNAME>", "reader", "specialized", "speed", "users"]
tier: 3
risk: "high"
estimated_tokens: 265
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["data", "analytics"]
quality_score: 0.58
description: "Launch RSVP speed reader for text"
source: "community"
tools: "Write, Bash, Read"
trigger: "command"
---
# Speed Reader

Launch the RSVP speed reader to display text one word at a time with Spritz-style ORP (Optimal Recognition Point) highlighting.

## Instructions

1. **Get the text:**
   - If `$ARGUMENTS` is provided, use that text
   - Otherwise, extract the main content from your **previous response** in this conversation

2. **Prepare the content:**
   - Strip markdown formatting (headers, bold, links, code blocks)
   - Keep clean, readable prose
   - Escape quotes and backslashes for JavaScript

3. **Write and launch:**
   - Read `~/.claude/skills/speed/data/reader.html`
   - Replace `<!-- CONTENT_PLACEHOLDER -->` with:
     ```html
     <script>window.SPEED_READER_CONTENT = "your escaped text";</script>
     <!-- CONTENT_PLACEHOLDER -->
     ```
   - Run: `open ~/.claude/skills/speed/data/reader.html`

4. **Confirm:** Tell the user it's opening. Mention `Space` to play/pause.

## Arguments
$ARGUMENTS
