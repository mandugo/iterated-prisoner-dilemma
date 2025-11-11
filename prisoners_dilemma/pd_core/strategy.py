"""Strategy protocol and helpers.

The framework keeps the interface intentionally small: a strategy is
stateful, must expose a :pyattr:`name` attribute and implement a
:func:`reset`, :func:`first_move` and :func:`next_move` method.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol
import random


Action = str


class Strategy(Protocol):
    """Protocol describing the behaviour of a Prisoner's Dilemma strategy."""

    name: str

    def reset(self) -> None:
        """Reset the internal state of the strategy before a new match."""

    def first_move(self, rng: random.Random) -> Action:
        """Return the first action to play."""

    def next_move(
        self,
        my_last: Optional[Action],
        opp_last: Optional[Action],
        rng: random.Random,
    ) -> Action:
        """Return the next action to play given the previous round state."""


@dataclass(slots=True)
class Memory:
    """Utility container storing the latest observed actions.

    Strategies with memory longer than a single step can keep a reference
    to a :class:`Memory` instance and read or append to the ``history``
    field.
    """

    history: list[tuple[Action, Action]]

    def append(self, mine: Action, opp: Action) -> None:
        self.history.append((mine, opp))

    def last(self) -> Optional[tuple[Action, Action]]:
        return self.history[-1] if self.history else None
