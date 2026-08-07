# Scribe Transcription Pipeline

Use AI Services Scribe when the input is already a file or storage object and the output should be a transcript JSON payload or transcript files.

## Skill Chain

- Primary: [../scribe/SKILL.md](../scribe/SKILL.md)
- Optional storage/download source: [../build-zoom-rest-api-app/SKILL.md](../build-zoom-rest-api-app/SKILL.md)
- Optional webhook hardening: [../setup-zoom-webhooks/SKILL.md](../setup-zoom-webhooks/SKILL.md)

## When to Use Scribe

Use `scribe` for:
- one uploaded file that should be transcribed immediately
- S3 archive transcription in the background
- post-processing exported media files into searchable transcript data

Do not use `scribe` for:
- live in-meeting media stream ingestion
- bot-style participant join and raw recording

For those, use:
- [../zoom-rtms/SKILL.md](../zoom-rtms/SKILL.md) for live media streams
- [../build-zoom-meeting-sdk-app/SKILL.md](../build-zoom-meeting-sdk-app/SKILL.md) for visible meeting bots

## Minimal Flow

```text
input file or storage prefix
  -> generate Build JWT
  -> choose fast mode or batch mode
  -> submit Scribe request
  -> receive transcript JSON or batch job state
  -> persist transcript output
```

## Typical Variants

1. Fast mode
   - one short file
   - immediate response needed
   - `POST /aiservices/scribe/transcribe`

2. Batch mode
   - long recordings or many files
   - `POST /aiservices/scribe/jobs`
   - monitor with polling or webhook notifications

3. Zoom recording re-transcription
   - use REST API to download or export recording files
   - feed those files into Scribe for your own transcript settings

## Common Failure Points

- wrong credential type (Build JWT vs normal OAuth token)
- choosing RTMS for offline archive transcription
- expired S3 credentials for batch jobs
- webhook signature verification implemented after JSON parsing instead of on raw body
