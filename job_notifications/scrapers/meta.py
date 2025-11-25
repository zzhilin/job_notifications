from __future__ import annotations

import httpx

from job_notifications.config import ScraperConfig
from job_notifications.normalization.models import NormalizedJob
from job_notifications.scrapers.base import Scraper


class MetaScraper(Scraper):
    name = "meta"

    def __init__(self, config: ScraperConfig, client: httpx.AsyncClient | None = None) -> None:
        super().__init__(config)
        self._client = client or httpx.AsyncClient(headers={"User-Agent": config.user_agent})

    async def fetch(self) -> list[NormalizedJob]:
        return [
            NormalizedJob(
                id="meta-1",
                title="Data Engineer",
                company="Meta",
                location="Menlo Park, CA",
                url=f"{self.config.meta_base_url}/jobs/1",
                source=self.name,
            )
        ]
