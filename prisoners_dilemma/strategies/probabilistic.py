"""Probabilistic strategies."""

from __future__ import annotations

import random

from ..pd_core.strategy import Action
from .base import StatelessStrategy


class RandomStrategy(StatelessStrategy):
    """Cooperate with a fixed probability ``p``."""

    def __init__(self, p: float = 0.5) -> None:
        if not (0.0 <= p <= 1.0):
            raise ValueError("p must be between 0 and 1")
        super().__init__(name=f"RAND({p:.2f})")
        self.p = p

    def next_move(self, my_last: Action | None, opp_last: Action | None, rng: random.Random) -> Action:
        return "C" if rng.random() <= self.p else "D"


class GenerousTitForTat(StatelessStrategy):
    """Tit For Tat with forgiveness probability ``forgive_p`` after defections."""

    def __init__(self, forgive_p: float = 0.1) -> None:
        if not (0.0 <= forgive_p <= 1.0):
            raise ValueError("forgive_p must be between 0 and 1")
        super().__init__(name=f"GTFT({forgive_p:.2f})")
        self.forgive_p = forgive_p

    def first_move(self, rng: random.Random) -> Action:
        return "C"

    def next_move(self, my_last: Action | None, opp_last: Action | None, rng: random.Random) -> Action:
        if opp_last != "D":
            return "C" if opp_last is None else opp_last
        return "C" if rng.random() <= self.forgive_p else "D"
