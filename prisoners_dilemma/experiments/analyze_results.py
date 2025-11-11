"""Utilities to analyse tournament results."""

from __future__ import annotations

from collections import Counter
from typing import Iterable

from ..pd_core.game import MatchOutcome


def cooperation_histogram(outcomes: Iterable[MatchOutcome]) -> dict[str, float]:
    counter = Counter({"A": 0.0, "B": 0.0})
    for outcome in outcomes:
        counter["A"] += outcome.cooperation_rate_a
        counter["B"] += outcome.cooperation_rate_b
    total = sum(counter.values())
    if total == 0:
        return {"A": 0.0, "B": 0.0}
    return {player: value / total for player, value in counter.items()}
