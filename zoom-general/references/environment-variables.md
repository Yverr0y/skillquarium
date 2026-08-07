# Cross-Product Environment Variables (Hub)

Use this file as a normalization map. Product-specific details are maintained in each product skill reference.

## Common `.env` keys

| Variable | Typical products | Where to find |
| --- | --- | --- |
| `ZOOM_CLIENT_ID` | OAuth, REST API, Team Chat, WebSockets, RTMS (OAuth mode), Contact Center APIs | Zoom Marketplace -> your app -> App Credentials |
| `ZOOM_CLIENT_SECRET` | OAuth, REST API, Team Chat, WebSockets, RTMS (OAuth mode), Contact Center APIs | Zoom Marketplace -> your app -> App Credentials |
| `ZOOM_ACCOUNT_ID` | Server-to-Server OAuth flows | Zoom Marketplace -> Server-to-Server OAuth app credentials |
| `ZOOM_REDIRECT_URI` | User-level OAuth apps | Zoom Marketplace -> OAuth redirect/allow list |
| `ZOOM_WEBHOOK_SECRET` / `WEBHOOK_SECRET_TOKEN` | Webhooks and event validation | Zoom Marketplace -> Event Subscriptions -> Secret Token |
| `ZOOM_SDK_KEY` / `ZOOM_SDK_SECRET` | Meeting SDK or SDK-based products | Zoom Marketplace -> SDK app credentials |
| `ZOOM_VIDEO_SDK_KEY` / `ZOOM_VIDEO_SDK_SECRET` | Video SDK and UI Toolkit | Zoom Marketplace -> Video SDK app credentials |
| `PROBE_JS_URL` / `PROBE_WASM_URL` | Probe SDK | Your app/CDN hosted Probe SDK assets (or bundler output paths) |
| `PROBE_DOMAIN` / `PROBE_CONNECT_TIMEOUT_MS` | Probe SDK | Product policy + Probe SDK diagnostics configuration |

## Product references

- [../zoom-apps-sdk/references/environment-variables.md](../zoom-apps-sdk/references/environment-variables.md)
- [../zoom-cobrowse-sdk/references/environment-variables.md](../zoom-cobrowse-sdk/references/environment-variables.md)
- [../build-zoom-meeting-sdk-app/references/environment-variables.md](../build-zoom-meeting-sdk-app/references/environment-variables.md)
- [../zoom-oauth/references/environment-variables.md](../zoom-oauth/references/environment-variables.md)
- [../build-zoom-rest-api-app/references/environment-variables.md](../build-zoom-rest-api-app/references/environment-variables.md)
- [../zoom-rtms/references/environment-variables.md](../zoom-rtms/references/environment-variables.md)
- [../build-zoom-team-chat-app/references/environment-variables.md](../build-zoom-team-chat-app/references/environment-variables.md)
- [../ui-toolkit/references/environment-variables.md](../ui-toolkit/references/environment-variables.md)
- [../build-zoom-video-sdk-app/references/environment-variables.md](../build-zoom-video-sdk-app/references/environment-variables.md)
- [../setup-zoom-webhooks/references/environment-variables.md](../setup-zoom-webhooks/references/environment-variables.md)
- [../setup-zoom-websockets/references/environment-variables.md](../setup-zoom-websockets/references/environment-variables.md)
- [../build-zoom-contact-center-app/references/environment-variables.md](../build-zoom-contact-center-app/references/environment-variables.md)
- [../build-zoom-phone-integration/references/environment-variables.md](../build-zoom-phone-integration/references/environment-variables.md)
- [../probe-sdk/references/environment-variables.md](../probe-sdk/references/environment-variables.md)

## Probe SDK note

- Probe SDK core diagnostics do not require Zoom OAuth/Marketplace credentials.
