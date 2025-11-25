from __future__ import annotations

import abc
from typing import Sequence

from job_notifications.config import ScraperConfig
from job_notifications.normalization.models import NormalizedJob


class Scraper(abc.ABC):
    def __init__(self, config: ScraperConfig) -> None:
        self.config = config

    @property
    @abc.abstractmethod
    def name(self) -> str: ...

    @abc.abstractmethod
    async def fetch(self) -> Sequence[NormalizedJob]:
        """Fetch raw job postings and return normalized objects."""
        raise NotImplementedError
