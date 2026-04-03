---
name: "conductor-manage"
tags: ["antigravity", "c:", "conductor", "frontend", "gemini", "instructions", "<YOUR_USERNAME>", "manage", "manager", "not", "resources", "safety", "skill", "specialized", "this", "track", "use", "users", "when"]
tier: 2
risk: "medium"
estimated_tokens: 323
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.62
date_added: "2026-02-27"
description: "Manage track lifecycle: archive, restore, delete, rename, and cleanup"
source: "community"
---
# Track Manager

Manage the complete track lifecycle including archiving, restoring, deleting, renaming, and cleaning up orphaned artifacts.

## Use this skill when

- Archiving, restoring, renaming, or deleting Conductor tracks
- Listing track status or cleaning orphaned artifacts
- Managing the track lifecycle across active, completed, and archived states

## Do not use this skill when

- Conductor is not initialized in the repository
- You lack permission to modify track metadata or files
- The task is unrelated to Conductor track management

## Instructions

- Verify `conductor/` structure and required files before proceeding.
- Determine the operation mode from arguments or interactive prompts.
- Confirm destructive actions (delete/cleanup) before applying.
- Update `tracks.md` and metadata consistently.
- If detailed steps are required, open `resources/implementation-playbook.md`.

## Safety

- Backup track data before delete operations.
- Avoid removing archived tracks without explicit approval.

## Resources

- `resources/implementation-playbook.md` for detailed modes, prompts, and workflows.
