---
name: "can-decode"
tags: ["decode, validation, video, audio, compatibility, browser"]
tier: 3
risk: "high"
estimated_tokens: 396
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["data", "analytics"]
quality_score: 0.67
description: "Check if a video can be decoded by the browser using Mediabunny"
metadata: ""
---
# Checking if a video can be decoded

Use Mediabunny to check if a video can be decoded by the browser before attempting to play it.

## The `canDecode()` function

This function can be copy-pasted into any project.

```tsx
import { Input, ALL_FORMATS, UrlSource } from "mediabunny";

export const canDecode = async (src: string) => {
  const input = new Input({
    formats: ALL_FORMATS,
    source: new UrlSource(src, {
      getRetryDelay: () => null,
    }),
  });

  try {
    await input.getFormat();
  } catch {
    return false;
  }

  const videoTrack = await input.getPrimaryVideoTrack();
  if (videoTrack && !(await videoTrack.canDecode())) {
    return false;
  }

  const audioTrack = await input.getPrimaryAudioTrack();
  if (audioTrack && !(await audioTrack.canDecode())) {
    return false;
  }

  return true;
};
```

## Usage

```tsx
const src = "https://remotion.media/video.mp4";
const isDecodable = await canDecode(src);

if (isDecodable) {
  console.log("Video can be decoded");
} else {
  console.log("Video cannot be decoded by this browser");
}
```

## Using with Blob

For file uploads or drag-and-drop, use `BlobSource`:

```tsx
import { Input, ALL_FORMATS, BlobSource } from "mediabunny";

export const canDecodeBlob = async (blob: Blob) => {
  const input = new Input({
    formats: ALL_FORMATS,
    source: new BlobSource(blob),
  });

  // Same validation logic as above
};
```
