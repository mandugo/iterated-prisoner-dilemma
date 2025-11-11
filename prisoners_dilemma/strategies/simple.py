"""Simple deterministic strategies."""

from __future__ import annotations

import random

from ..pd_core.strategy import Action
from .base import MemoryOneStrategy, StatelessStrategy


class AllCooperate(StatelessStrategy):
    """Always cooperate."""

    def __init__(self) -> None:
        super().__init__(name="ALLC")

    def next_move(self, my_last: Action | None, opp_last: Action | None, rng: random.Random) -> Action:
        return "C"


class AllDefect(StatelessStrategy):
    """Always defect."""

    def __init__(self) -> None:
        super().__init__(name="ALLD")

    def next_move(self, my_last: Action | None, opp_last: Action | None, rng: random.Random) -> Action:
        return "D"


class TitForTat(StatelessStrategy):
    """Cooperate first, then mirror the opponent's last action."""

    def __init__(self) -> None:
        super().__init__(name="TFT")

    def first_move(self, rng: random.Random) -> Action:
        return "C"

    def next_move(self, my_last: Action | None, opp_last: Action | None, rng: random.Random) -> Action:
        return "C" if opp_last is None else opp_last


class TitForTwoTats(StatelessStrategy):
    """Defect only after two consecutive defections from the opponent."""

    def __init__(self) -> None:
        super().__init__(name="TF2T")
        self._defection_streak = 0

    def reset(self) -> None:
        self._defection_streak = 0

    def first_move(self, rng: random.Random) -> Action:
        self._defection_streak = 0
        return "C"

    def next_move(self, my_last: Action | None, opp_last: Action | None, rng: random.Random) -> Action:
        if opp_last == "D":
            self._defection_streak += 1
        else:
            self._defection_streak = 0
        return "D" if self._defection_streak >= 2 else "C"


class GrimTrigger(StatelessStrategy):
    """Cooperate until the opponent defects once, then always defect."""

    def __init__(self) -> None:
        super().__init__(name="GRIM")
        self._betrayed = False

    def reset(self) -> None:
        self._betrayed = False

    def first_move(self, rng: random.Random) -> Action:
        self._betrayed = False
        return "C"

    def next_move(self, my_last: Action | None, opp_last: Action | None, rng: random.Random) -> Action:
        if opp_last == "D":
            self._betrayed = True
        return "D" if self._betrayed else "C"


class Pavlov(MemoryOneStrategy):
    """Win-stay, lose-shift strategy."""

    def __init__(self) -> None:
        super().__init__(name="PAVLOV", initial_action="C")

    def next_move(self, my_last: Action | None, opp_last: Action | None, rng: random.Random) -> Action:
        if my_last is None or opp_last is None:
            return "C"
        if my_last == opp_last:
            return my_last
        return "D" if my_last == "C" else "C"
