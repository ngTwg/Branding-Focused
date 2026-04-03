---
name: "get-audio-duration"
tags: ["duration, audio, length, time, seconds, mp3, wav"]
tier: 3
risk: "high"
estimated_tokens: 338
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["data", "analytics"]
quality_score: 0.72
description: "Getting the duration of an audio file in seconds with Mediabunny"
metadata: ""
---
# Getting audio duration with Mediabunny

Mediabunny can extract the duration of an audio file. It works in browser, Node.js, and Bun environments.

## Getting audio duration

```tsx
import { Input, ALL_FORMATS, UrlSource } from "mediabunny";

export const getAudioDuration = async (src: string) => {
  const input = new Input({
    formats: ALL_FORMATS,
    source: new UrlSource(src, {
      getRetryDelay: () => null,
    }),
  });

  const durationInSeconds = await input.computeDuration();
  return durationInSeconds;
};
```

## Usage

```tsx
const duration = await getAudioDuration("https://remotion.media/audio.mp3");
console.log(duration); // e.g. 180.5 (seconds)
```

## Using with local files

For local files, use `FileSource` instead of `UrlSource`:

```tsx
import { Input, ALL_FORMATS, FileSource } from "mediabunny";

const input = new Input({
  formats: ALL_FORMATS,
  source: new FileSource(file), // File object from input or drag-drop
});

const durationInSeconds = await input.computeDuration();
```

## Using with staticFile in Remotion

```tsx
import { staticFile } from "remotion";

const duration = await getAudioDuration(staticFile("audio.mp3"));
```
