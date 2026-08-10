# Flutter Video Sessions

Use this flow when you are building custom real-time video sessions in a Flutter mobile app.

## When to Use

- You need full control over UI/UX (not Zoom Meeting UI).
- You are building iOS/Android mobile session experiences in Flutter.
- You need helper-driven features such as chat, share, recording, or transcription.

## Skill Chain

1. [video-sdk/flutter](../build-zoom-video-sdk-app/SKILL.md)
2. [zoom-oauth](../zoom-oauth/SKILL.md)

## Typical Flow

1. Backend signs short-lived Video SDK JWT.
2. Flutter app initializes SDK and binds event listeners.
3. App joins session and activates media/helpers.
4. App leaves and cleans up explicitly.

## References

- [Flutter Video SDK Skill](../build-zoom-video-sdk-app/SKILL.md)
- [Lifecycle Workflow](../build-zoom-video-sdk-app/flutter/concepts/lifecycle-workflow.md)
- [Session Join Pattern](../build-zoom-video-sdk-app/flutter/examples/session-join-pattern.md)
