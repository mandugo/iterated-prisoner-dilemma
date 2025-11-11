"""Noise models applied to strategies' chosen actions."""

from __future__ import annotations

from dataclasses import dataclass
import random

from .strategy import Action


def flip(action: Action) -> Action:
    return "D" if action == "C" else "C"


@dataclass(slots=True)
class Noise:
    """Simple bit-flip noise model."""

    epsilon: float = 0.0

    def apply(self, action: Action, rng: random.Random) -> Action:
        if self.epsilon <= 0:
            return action
        if rng.random() <= self.epsilon:
            return flip(action)
        return action
