from __future__ import annotations

import logging
from email.message import EmailMessage

import aiosmtplib

from job_notifications.config import EmailConfig
from job_notifications.normalization.models import NormalizedJob

logger = logging.getLogger(__name__)


class EmailNotifier:
    def __init__(self, config: EmailConfig) -> None:
        self.config = config

    async def notify(self, jobs: list[NormalizedJob]) -> None:
        if not self.config.enabled:
            logger.info("Email notifications disabled; skipping send")
            return
        message = self._build_message(jobs)
        await aiosmtplib.send(
            message,
            hostname=self.config.host,
            port=self.config.port,
            username=self.config.username,
            password=self.config.password,
            start_tls=self.config.use_tls,
        )

    def _build_message(self, jobs: list[NormalizedJob]) -> EmailMessage:
        msg = EmailMessage()
        msg["From"] = self.config.from_email
        msg["To"] = self.config.to_email
        msg["Subject"] = f"{len(jobs)} new job(s) discovered"
        body_lines = [f"- {job.title} at {job.company} ({job.url})" for job in jobs]
        msg.set_content("\n".join(body_lines))
        return msg
