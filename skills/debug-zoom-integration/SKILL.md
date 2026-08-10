---
name: debug-zoom-integration
description: Use when isolating failures.
---

# Debug Zoom Integration

Use this skill when the user already built something and it is failing.

## Triage Order

1. Auth and app configuration
2. Request construction or event verification
3. SDK initialization or platform mismatch
4. Media/session behavior
5. Client platform and capability assumptions

## Evidence To Request

- Exact error text
- Platform and SDK/runtime
- Relevant request or payload sample
- What worked versus what failed
- Whether the issue is reproducible or intermittent

## Reference Routing

- [oauth](../zoom-oauth/SKILL.md)
- [rest-api](../build-zoom-rest-api-app/SKILL.md)
- [webhooks](../setup-zoom-webhooks/SKILL.md)
- [meeting-sdk](../build-zoom-meeting-sdk-app/SKILL.md)
- [video-sdk](../build-zoom-video-sdk-app/SKILL.md)
- [rtms](../zoom-rtms/SKILL.md)

## Output

- Most likely failing layer
- Ranked hypotheses
- Short fix plan
- Verification steps
