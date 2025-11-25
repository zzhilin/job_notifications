# Job Notifications

Async Python 3.10+ agent that scrapes job boards, normalizes postings, applies heuristic filtering, persists results in SQLite, and optionally delivers email notifications.

## Features
- Async scheduler with jittered intervals for pipeline runs
- Scraper stubs for Greenhouse, Lever, Meta, Google, and Uber (HTTP/Playwright ready)
- Normalized job model with persistence to SQLite (memory or file)
- Heuristic filter layer for quick relevance scoring
- Email notifier using SMTP (disabled by default)
- CLI entrypoint and Dockerfile for containerized execution

## Getting Started
1. Install dependencies (dev extras include pytest):
   ```bash
   pip install -e .[dev]
   ```
2. Run tests:
   ```bash
   pytest
   ```
3. Start the agent locally (defaults to in-memory SQLite and disabled email):
   ```bash
   job-notifications --interval 120 --jitter 10
   ```

## Configuration
Configuration is defined in `job_notifications/config.py` and may be overridden via the CLI or by calling `load_settings()` with overrides. Email is disabled by default to avoid accidental sends.

## Docker
Build and run using the provided Dockerfile:
```bash
docker build -t job-notifications .
docker run --rm job-notifications
```
