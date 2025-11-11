from prisoners_dilemma.pd_core.game import MatchOutcome
from prisoners_dilemma.pd_core.metrics import AggregatedMetrics, aggregate


def test_aggregate_empty() -> None:
    metrics = aggregate([])
    assert metrics == AggregatedMetrics(0.0, 0.0)


def test_aggregate_mean() -> None:
    outcomes = [
        MatchOutcome(10, 5, 5, 2.5, 0.5, 0.2),
        MatchOutcome(6, 6, 3, 3, 0.3, 0.4),
    ]
    metrics = aggregate(outcomes)
    assert metrics.mean_payoff == (5 + 2.5 + 3 + 3) / 4
    assert metrics.cooperation_rate == (0.5 + 0.2 + 0.3 + 0.4) / 4
