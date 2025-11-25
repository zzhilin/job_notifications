import asyncio

import pytest

from job_notifications.normalization.models import NormalizedJob
from job_notifications.persistence.sqlite import JobStore


@pytest.mark.asyncio
async def test_save_if_new_and_deduplicate(tmp_path):
    db_path = tmp_path / "jobs.db"
    store = JobStore(str(db_path))
    job = NormalizedJob(
        id="1",
        title="Engineer",
        company="TestCo",
        location="Remote",
        url="https://example.com/jobs/1",
        source="test",
    )
    first = await store.save_if_new(job)
    second = await store.save_if_new(job)
    await store.close()
    assert first is True
    assert second is False
