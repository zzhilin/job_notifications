from __future__ import annotations

import httpx

from job_notifications.config import ScraperConfig
from job_notifications.normalization.models import NormalizedJob
from job_notifications.scrapers.base import Scraper


class UberScraper(Scraper):
    name = "uber"

    def __init__(self, config: ScraperConfig, client: httpx.AsyncClient | None = None) -> None:
        super().__init__(config)
        self._client = client or httpx.AsyncClient(headers={"User-Agent": config.user_agent})

    async def fetch(self) -> list[NormalizedJob]:
        return [
            NormalizedJob(
                id="uber-1",
                title="Mobile Engineer",
                company="Uber",
                location="New York, NY",
                url=f"{self.config.uber_base_url}/jobs/1",
                source=self.name,
            )
        ]
