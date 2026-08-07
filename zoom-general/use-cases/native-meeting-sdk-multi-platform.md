# Native Meeting SDK Multi-Platform Delivery

Use this flow when you need the same embedded meeting product capability across multiple native stacks (Android, iOS, macOS, Unreal) while keeping behavior and auth patterns consistent.

## When to Use

- You are shipping a shared meeting feature set across multiple native clients.
- You need consistent auth/signature and role policy across platforms.
- You need version-drift guardrails and staged rollout checks per platform.

## Skill Chain

1. [meeting-sdk](../build-zoom-meeting-sdk-app/SKILL.md)
2. [meeting-sdk/android](../build-zoom-meeting-sdk-app/SKILL.md)
3. [meeting-sdk/ios](../build-zoom-meeting-sdk-app/SKILL.md)
4. [meeting-sdk/macos](../build-zoom-meeting-sdk-app/SKILL.md)
5. [meeting-sdk/unreal](../build-zoom-meeting-sdk-app/SKILL.md)
6. [oauth](../zoom-oauth/SKILL.md)

## Typical Flow

1. Standardize server-side signing and role policy once.
2. Validate default UI join/start baseline on each platform.
3. Add platform-specific custom UI features only after baseline parity.
4. Maintain a version matrix and run upgrade checks per platform before release.
5. Track contradictions between wrapper docs, package artifacts, and API references.

## References

- [Meeting SDK Root Skill](../build-zoom-meeting-sdk-app/SKILL.md)
- [Android Reference Map](../build-zoom-meeting-sdk-app/android/references/android-reference-map.md)
- [iOS Reference Map](../build-zoom-meeting-sdk-app/ios/references/ios-reference-map.md)
- [macOS Reference Map](../build-zoom-meeting-sdk-app/macos/references/macos-reference-map.md)
- [Unreal Reference Map](../build-zoom-meeting-sdk-app/unreal/references/unreal-reference-map.md)
