from __future__ import annotations

import httpx

from job_notifications.config import ScraperConfig
from job_notifications.normalization.models import NormalizedJob
from job_notifications.scrapers.base import Scraper


class LeverScraper(Scraper):
    name = "lever"

    def __init__(self, config: ScraperConfig, client: httpx.AsyncClient | None = None) -> None:
        super().__init__(config)
        self._client = client or httpx.AsyncClient(headers={"User-Agent": config.user_agent})

    async def fetch(self) -> list[NormalizedJob]:
        return [
            NormalizedJob(
                id="lever-1",
                title="Backend Engineer",
                company="ExampleCo",
                location="Hybrid",
                url=f"{self.config.lever_base_url}/postings/example/1",
                source=self.name,
            )
        ]
