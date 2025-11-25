from job_notifications import config


def test_load_settings_override():
    settings = config.load_settings(scheduler={"interval_seconds": 5, "jitter_seconds": 1})
    assert settings.scheduler.interval_seconds == 5
    assert settings.scheduler.jitter_seconds == 1
