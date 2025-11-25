from __future__ import annotations

import asyncio
import contextlib
import logging
import random
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class ScheduledTask:
    name: str
    coro_factory: Callable[[], Awaitable[Any]]
    interval_seconds: float
    jitter_seconds: float = 0.0


def compute_delay(interval: float, jitter: float) -> float:
    jitter = max(0.0, jitter)
    if interval <= 0:
        raise ValueError("Interval must be positive")
    return interval + random.uniform(-jitter, jitter)


class AsyncScheduler:
    """Simple asyncio scheduler with jittered intervals and graceful shutdown."""

    def __init__(self) -> None:
        self._tasks: list[ScheduledTask] = []
        self._running_tasks: list[asyncio.Task[Any]] = []
        self._shutdown_event = asyncio.Event()

    def add_task(self, task: ScheduledTask) -> None:
        logger.debug("Registering task %s", task.name)
        self._tasks.append(task)

    async def _runner(self, scheduled: ScheduledTask) -> None:
        logger.info("Scheduler starting task %s", scheduled.name)
        while not self._shutdown_event.is_set():
            delay = compute_delay(scheduled.interval_seconds, scheduled.jitter_seconds)
            logger.debug("Task %s sleeping for %.2fs", scheduled.name, delay)
            await asyncio.sleep(delay)
            if self._shutdown_event.is_set():
                break
            try:
                await scheduled.coro_factory()
            except asyncio.CancelledError:
                raise
            except Exception:  # pragma: no cover - log path
                logger.exception("Task %s failed", scheduled.name)

    async def run(self) -> None:
        if not self._tasks:
            logger.warning("No scheduled tasks to run")
            return
        for task in self._tasks:
            self._running_tasks.append(asyncio.create_task(self._runner(task)))
        try:
            await self._shutdown_event.wait()
        finally:
            await self.shutdown()

    async def shutdown(self) -> None:
        if self._shutdown_event.is_set():
            logger.debug("Shutdown already in progress")
        self._shutdown_event.set()
        for task in self._running_tasks:
            task.cancel()
        for task in self._running_tasks:
            with contextlib.suppress(asyncio.CancelledError):
                await task
        self._running_tasks.clear()
        logger.info("Scheduler stopped")


async def run_once(task: ScheduledTask) -> None:
    """Utility for tests to run a scheduled task once without a loop."""

    await task.coro_factory()
