"""Collection of baseline strategies for the Iterated Prisoner's Dilemma."""

from .simple import AllCooperate, AllDefect, GrimTrigger, Pavlov, TitForTat, TitForTwoTats
from .probabilistic import GenerousTitForTat, RandomStrategy

__all__ = [
    "AllCooperate",
    "AllDefect",
    "GrimTrigger",
    "Pavlov",
    "TitForTat",
    "TitForTwoTats",
    "GenerousTitForTat",
    "RandomStrategy",
]
