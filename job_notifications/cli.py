from __future__ import annotations

import argparse
import asyncio
import logging
import signal

from job_notifications.config import DEFAULT_SETTINGS, load_settings
from job_notifications.lifecycle.agent import Agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the job notifications agent")
    parser.add_argument(
        "--interval",
        type=float,
        default=DEFAULT_SETTINGS.scheduler.interval_seconds,
        help="Base interval between pipeline runs",
    )
    parser.add_argument(
        "--jitter",
        type=float,
        default=DEFAULT_SETTINGS.scheduler.jitter_seconds,
        help="Maximum jitter to add to the interval",
    )
    parser.add_argument(
        "--db-path", type=str, default=DEFAULT_SETTINGS.database.path, help="SQLite database path"
    )
    parser.add_argument(
        "--email-enabled",
        action="store_true",
        help="Enable email notifications (requires SMTP configuration)",
    )
    return parser.parse_args()


async def _run_agent(agent: Agent) -> None:
    loop = asyncio.get_running_loop()
    stop = asyncio.Event()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop.set)

    runner = asyncio.create_task(agent.start())
    await stop.wait()
    await agent.shutdown()
    runner.cancel()


def main() -> None:
    args = parse_args()
    settings = load_settings(
        scheduler={
            "interval_seconds": args.interval,
            "jitter_seconds": args.jitter,
        },
        database={"path": args.db_path},
        email={"enabled": args.email_enabled},
    )
    agent = Agent(settings)
    asyncio.run(_run_agent(agent))


if __name__ == "__main__":
    main()
