from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, HttpUrl


class NormalizedJob(BaseModel):
    id: str
    title: str
    company: str
    location: str | None = None
    url: HttpUrl
    source: str
    posted_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    def key(self) -> str:
        return f"{self.source}:{self.id}"
