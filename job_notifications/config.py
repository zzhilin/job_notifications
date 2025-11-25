from __future__ import annotations

from pydantic import BaseModel, Field


class SchedulerConfig(BaseModel):
    interval_seconds: float = Field(60.0, description="Base interval between runs")
    jitter_seconds: float = Field(5.0, ge=0.0, description="Max jitter applied to the interval")


class ScraperConfig(BaseModel):
    greenhouse_base_url: str = "https://boards.greenhouse.io"
    lever_base_url: str = "https://api.lever.co/v1"
    meta_base_url: str = "https://www.metacareers.com"
    google_base_url: str = "https://careers.google.com"
    uber_base_url: str = "https://www.uber.com/careers"
    user_agent: str = (
        "job-notifications/0.1 (+https://example.com; contact=ops@example.com)"
    )


class DatabaseConfig(BaseModel):
    path: str = Field(
        ":memory:",
        description="SQLite connection string; use :memory: for ephemeral runs",
    )


class EmailConfig(BaseModel):
    enabled: bool = False
    host: str = "smtp.example.com"
    port: int = 587
    username: str | None = None
    password: str | None = None
    from_email: str = "jobs@example.com"
    to_email: str = "recipient@example.com"
    use_tls: bool = True


class Settings(BaseModel):
    scheduler: SchedulerConfig = Field(default_factory=SchedulerConfig)
    scrapers: ScraperConfig = Field(default_factory=ScraperConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    email: EmailConfig = Field(default_factory=EmailConfig)


DEFAULT_SETTINGS = Settings()


def load_settings(**overrides: object) -> Settings:
    """Load Settings with optional overrides for tests or CLIs.

    This function keeps dependencies light while allowing injection in tests.
    """

    return DEFAULT_SETTINGS.model_copy(update=overrides)
