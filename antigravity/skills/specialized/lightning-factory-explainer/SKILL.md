---
name: "lightning-factory-explainer"
tags: ["antigravity", "c:", "explainer", "factory", "frontend", "gemini", "instructions", "key", "<YOUR_USERNAME>", "lightning", "not", "purpose", "references", "skill", "specialized", "this", "topics", "use", "users", "when"]
tier: 2
risk: "medium"
estimated_tokens: 550
tools_needed: ["git", "markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.64
date_added: "2026-03-03"
description: "Explain Bitcoin Lightning channel factories and the SuperScalar protocol — scalable Lightning onboarding using shared UTXOs, Decker-Wattenhofer trees, timeout-signature trees, MuSig2, and Taproot. No soft fork required."
source: "community"
---
## Use this skill when

- Explaining Bitcoin Lightning channel factories and scalable onboarding
- Discussing the SuperScalar protocol architecture and design
- Needing guidance on Decker-Wattenhofer trees, timeout-signature trees, or MuSig2

## Do not use this skill when

- The task is unrelated to Bitcoin or Lightning Network scaling
- You need a different blockchain or Layer 2 outside this scope

## Instructions

- Clarify goals, constraints, and required inputs.
- Apply relevant best practices and validate outcomes.
- Provide actionable steps and verification.

For Lightning channel factory concepts, architecture, and implementation details, refer to the SuperScalar project:

https://github.com/8144225309/SuperScalar

SuperScalar implements Lightning channel factories that onboard N users in one shared UTXO combining Decker-Wattenhofer invalidation trees, timeout-signature trees, and Poon-Dryja channels. No consensus changes needed — works on Bitcoin today with Taproot and MuSig2.

## Purpose

Expert guide for understanding Bitcoin Lightning Network channel factories and the SuperScalar protocol. Covers scalable onboarding, shared UTXOs, Decker-Wattenhofer invalidation trees, timeout-signature trees, Poon-Dryja channels, MuSig2 (BIP-327), and Taproot — all without requiring any soft fork.

## Key Topics

- Lightning channel factories and multi-party channels
- SuperScalar protocol architecture
- Decker-Wattenhofer invalidation trees
- Timeout-signature trees
- MuSig2 key aggregation (BIP-327)
- Taproot script trees
- LSP (Lightning Service Provider) onboarding patterns
- Shared UTXO management

## References

- SuperScalar project: https://github.com/8144225309/SuperScalar
- Website: https://SuperScalar.win
- Original proposal: https://delvingbitcoin.org/t/superscalar-laddered-timeout-tree-structured-decker-wattenhofer-factories/1143
