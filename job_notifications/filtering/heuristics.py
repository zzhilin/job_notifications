from __future__ import annotations

from job_notifications.normalization.models import NormalizedJob

KEYWORDS = {"engineer", "developer", "data", "ml", "ai"}


class HeuristicFilter:
    def __init__(self, keywords: set[str] | None = None) -> None:
        self.keywords = {kw.lower() for kw in (keywords or KEYWORDS)}

    def is_relevant(self, job: NormalizedJob) -> bool:
        title = job.title.lower()
        return any(keyword in title for keyword in self.keywords)
