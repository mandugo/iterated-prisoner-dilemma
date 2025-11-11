"""Player abstraction binding a strategy instance to runtime metadata."""

from __future__ import annotations

from dataclasses import dataclass, field
import random
from typing import Optional

from .strategy import Action, Strategy


@dataclass(slots=True)
class Player:
    """Container pairing a :class:`Strategy` with metadata.

    Parameters
    ----------
    strategy:
        The strategy instance controlling the player.
    name:
        Optional override for the public display name.  Defaults to the
        strategy ``name`` attribute.
    seed:
        Optional dedicated seed for the player's random number generator.
    """

    strategy: Strategy
    name: Optional[str] = None
    seed: Optional[int] = None
    _rng: random.Random = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._rng = random.Random(self.seed)

    @property
    def rng(self) -> random.Random:
        """Return a random number generator scoped to this player."""

        return self._rng

    @property
    def display_name(self) -> str:
        return self.name or self.strategy.name

    def reset(self) -> None:
        """Reset the strategy and RNG before starting a match."""

        self.strategy.reset()
        if self.seed is not None:
            self._rng.seed(self.seed)

    def first_move(self) -> Action:
        return self.strategy.first_move(self._rng)

    def next_move(self, my_last: Action, opp_last: Action) -> Action:
        return self.strategy.next_move(my_last, opp_last, self._rng)
