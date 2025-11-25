from __future__ import annotations

import logging
from typing import Iterable

from job_notifications.config import Settings
from job_notifications.filtering.heuristics import HeuristicFilter
from job_notifications.normalization.models import NormalizedJob
from job_notifications.notifications.email_service import EmailNotifier
from job_notifications.persistence.sqlite import JobStore
from job_notifications.scrapers import greenhouse, google, lever, meta, uber
from job_notifications.scrapers.base import Scraper
from job_notifications.utils.scheduler import AsyncScheduler, ScheduledTask

logger = logging.getLogger(__name__)


class Agent:
    """Orchestrates scraper execution, normalization, filtering, and notifications."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.store = JobStore(settings.database.path)
        self.filter = HeuristicFilter()
        self.notifier = EmailNotifier(settings.email)
        self.scheduler = AsyncScheduler()
        self.scrapers: list[Scraper] = [
            greenhouse.GreenhouseScraper(settings.scrapers),
            lever.LeverScraper(settings.scrapers),
            meta.MetaScraper(settings.scrapers),
            google.GoogleScraper(settings.scrapers),
            uber.UberScraper(settings.scrapers),
        ]

    async def _run_pipeline(self) -> None:
        jobs = await self._collect_jobs()
        new_jobs = await self._persist_new_jobs(jobs)
        if not new_jobs:
            logger.info("No new jobs discovered")
            return
        filtered = [job for job in new_jobs if self.filter.is_relevant(job)]
        if not filtered:
            logger.info("No jobs matched filter criteria")
            return
        await self.notifier.notify(filtered)

    async def _collect_jobs(self) -> list[NormalizedJob]:
        collected: list[NormalizedJob] = []
        for scraper in self.scrapers:
            try:
                results = await scraper.fetch()
            except Exception:  # pragma: no cover - log path
                logger.exception("Scraper %s failed", scraper.name)
                continue
            collected.extend(results)
        return collected

    async def _persist_new_jobs(
        self, jobs: Iterable[NormalizedJob]
    ) -> list[NormalizedJob]:
        saved: list[NormalizedJob] = []
        for job in jobs:
            is_new = await self.store.save_if_new(job)
            if is_new:
                saved.append(job)
        return saved

    async def start(self) -> None:
        logger.info("Starting agent")
        self.scheduler.add_task(
            ScheduledTask(
                name="pipeline",
                coro_factory=self._run_pipeline,
                interval_seconds=self.settings.scheduler.interval_seconds,
                jitter_seconds=self.settings.scheduler.jitter_seconds,
            )
        )
        await self.scheduler.run()

    async def shutdown(self) -> None:
        logger.info("Shutting down agent")
        await self.scheduler.shutdown()
        await self.store.close()
