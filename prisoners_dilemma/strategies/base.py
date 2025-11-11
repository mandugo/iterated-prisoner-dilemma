"""Base classes for strategies."""

from __future__ import annotations

from dataclasses import dataclass, field
import random

from ..pd_core.strategy import Action, Strategy


@dataclass
class StatelessStrategy:
    name: str

    def reset(self) -> None:  # pragma: no cover - nothing to reset
        pass

    def first_move(self, rng: random.Random) -> Action:
        return self.next_move(None, None, rng)


@dataclass
class MemoryOneStrategy:
    name: str
    initial_action: Action = "C"
    _last_action: Action = field(init=False, default="C")

    def reset(self) -> None:
        self._last_action = self.initial_action

    def first_move(self, rng: random.Random) -> Action:
        self._last_action = self.initial_action
        return self._last_action

    def record(self, action: Action) -> None:
        self._last_action = action
