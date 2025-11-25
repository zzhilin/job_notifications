from __future__ import annotations

import asyncio
import sqlite3

from job_notifications.normalization.models import NormalizedJob


SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
    key TEXT PRIMARY KEY,
    id TEXT NOT NULL,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    location TEXT,
    url TEXT NOT NULL,
    source TEXT NOT NULL,
    posted_at TEXT,
    metadata TEXT
);
"""


class JobStore:
    def __init__(self, path: str) -> None:
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._conn.execute("PRAGMA journal_mode=WAL;")
        self._conn.execute(SCHEMA)
        self._conn.commit()

    async def save_if_new(self, job: NormalizedJob) -> bool:
        return await asyncio.to_thread(self._save_if_new_sync, job)

    def _save_if_new_sync(self, job: NormalizedJob) -> bool:
        cursor = self._conn.cursor()
        try:
            cursor.execute(
                "INSERT OR IGNORE INTO jobs (key, id, title, company, location, url, source, posted_at, metadata)"
                " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    job.key(),
                    job.id,
                    job.title,
                    job.company,
                    job.location,
                    str(job.url),
                    job.source,
                    job.posted_at.isoformat() if job.posted_at else None,
                    job.model_dump_json(),
                ),
            )
            self._conn.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()

    async def fetch_all(self) -> list[NormalizedJob]:
        return await asyncio.to_thread(self._fetch_all_sync)

    def _fetch_all_sync(self) -> list[NormalizedJob]:
        cursor = self._conn.cursor()
        try:
            rows = cursor.execute(
                "SELECT id, title, company, location, url, source, posted_at, metadata FROM jobs"
            ).fetchall()
            jobs: list[NormalizedJob] = []
            for row in rows:
                jobs.append(
                    NormalizedJob.model_validate_json(
                        row[7]
                    )
                )
            return jobs
        finally:
            cursor.close()

    async def close(self) -> None:
        await asyncio.to_thread(self._conn.close)
