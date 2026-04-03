---
name: "transcribe-captions"
tags: ["captions, transcribe, whisper, audio, speech-to-text"]
tier: 2
risk: "medium"
estimated_tokens: 212
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.51
description: "Transcribing audio to generate captions in Remotion"
metadata: ""
---
# Transcribing audio

Remotion provides several built-in options for transcribing audio to generate captions:

- `@remotion/install-whisper-cpp` - Transcribe locally on a server using Whisper.cpp. Fast and free, but requires server infrastructure.
  https://remotion.dev/docs/install-whisper-cpp

- `@remotion/whisper-web` - Transcribe in the browser using WebAssembly. No server needed and free, but slower due to WASM overhead.
  https://remotion.dev/docs/whisper-web

- `@remotion/openai-whisper` - Use OpenAI Whisper API for cloud-based transcription. Fast and no server needed, but requires payment.
  https://remotion.dev/docs/openai-whisper/openai-whisper-api-to-captions
