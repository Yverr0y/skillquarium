---
name: choose-zoom-approach
description: Use when choosing architecture.
---

# Choose Zoom Approach

Pick the smallest correct Zoom surface for the job, then layer in only the supporting pieces that are actually required.

## Decision Framework

| Problem Type | Primary Zoom Surface |
|---|---|
| Deterministic backend automation, account management, reporting, scheduled jobs | [rest-api](../build-zoom-rest-api-app/SKILL.md) |
| Event delivery to your backend | [webhooks](../setup-zoom-webhooks/SKILL.md) or [websockets](../setup-zoom-websockets/SKILL.md) |
| Embed Zoom meetings into your app | [meeting-sdk](../build-zoom-meeting-sdk-app/SKILL.md) |
| Build a fully custom video experience | [video-sdk](../build-zoom-video-sdk-app/SKILL.md) |
| Build inside the Zoom client | [zoom-apps-sdk](../zoom-apps-sdk/SKILL.md) |
| Real-time media extraction or meeting bots | [rtms](../zoom-rtms/SKILL.md) plus [meeting-sdk](../build-zoom-meeting-sdk-app/SKILL.md) when needed |
| Phone workflows | [phone](../build-zoom-phone-integration/SKILL.md) |
| Contact Center or Virtual Agent flows | [contact-center](../build-zoom-contact-center-app/SKILL.md) or [virtual-agent](../build-zoom-virtual-agent/SKILL.md) |

## Guardrails

- Do not recommend Video SDK when the user actually needs Zoom meeting semantics.
- Do not recommend Meeting SDK when the user needs a fully custom session product.
- Keep deterministic backend automation in REST APIs and event-driven code.

## What To Produce

- One recommended path
- Minimum supporting components
- Hard constraints and tradeoffs
- Immediate next implementation step
