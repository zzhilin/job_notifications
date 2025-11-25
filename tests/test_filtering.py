from job_notifications.filtering.heuristics import HeuristicFilter
from job_notifications.normalization.models import NormalizedJob


def test_heuristic_filter_matches_keyword():
    filt = HeuristicFilter({"ai"})
    job = NormalizedJob(
        id="1",
        title="AI Engineer",
        company="TestCo",
        url="https://example.com",
        source="test",
    )
    assert filt.is_relevant(job)


def test_heuristic_filter_no_match():
    filt = HeuristicFilter({"data"})
    job = NormalizedJob(
        id="1",
        title="Marketing Manager",
        company="TestCo",
        url="https://example.com",
        source="test",
    )
    assert not filt.is_relevant(job)
