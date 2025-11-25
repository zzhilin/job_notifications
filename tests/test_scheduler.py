import pytest

from job_notifications.utils.scheduler import compute_delay


def test_compute_delay_within_bounds(monkeypatch):
    monkeypatch.setattr("random.uniform", lambda a, b: b)  # choose upper bound
    delay = compute_delay(10, 2)
    assert delay == 12


def test_compute_delay_negative_interval():
    with pytest.raises(ValueError):
        compute_delay(0, 1)
