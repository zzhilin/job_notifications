from __future__ import annotations

import httpx

from job_notifications.config import ScraperConfig
from job_notifications.normalization.models import NormalizedJob
from job_notifications.scrapers.base import Scraper


class GreenhouseScraper(Scraper):
    name = "greenhouse"

    def __init__(self, config: ScraperConfig, client: httpx.AsyncClient | None = None) -> None:
        super().__init__(config)
        self._client = client or httpx.AsyncClient(headers={"User-Agent": config.user_agent})

    async def fetch(self) -> list[NormalizedJob]:
        # Placeholder implementation. Real implementation would scrape via HTTP/Playwright.
        return [
            NormalizedJob(
                id="gh-1",
                title="Software Engineer",
                company="ExampleCo",
                location="Remote",
                url=f"{self.config.greenhouse_base_url}/example/jobs/1",
                source=self.name,
            )
        ]
