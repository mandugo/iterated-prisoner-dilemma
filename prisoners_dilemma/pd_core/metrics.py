"""Metrics helpers for aggregating match outcomes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .game import MatchOutcome


@dataclass(frozen=True)
class AggregatedMetrics:
    mean_payoff: float
    cooperation_rate: float


def aggregate(outcomes: Iterable[MatchOutcome]) -> AggregatedMetrics:
    outcomes_list = list(outcomes)
    if not outcomes_list:
        return AggregatedMetrics(0.0, 0.0)
    mean_payoff = sum(o.mean_payoff_a + o.mean_payoff_b for o in outcomes_list) / (
        2 * len(outcomes_list)
    )
    cooperation_rate = sum(
        o.cooperation_rate_a + o.cooperation_rate_b for o in outcomes_list
    ) / (2 * len(outcomes_list))
    return AggregatedMetrics(mean_payoff, cooperation_rate)
