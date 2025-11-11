"""Top-level package for the Iterated Prisoner's Dilemma framework.

The package exposes high-level helpers to build and run experiments
involving Prisoner's Dilemma strategies.  See the module level
documentation for more details.
"""

from .pd_core.game import IteratedMatch, MatchLog, PayoffMatrix
from .pd_core.noise import Noise
from .pd_core.tournament import RoundRobinTournament

__all__ = [
    "IteratedMatch",
    "MatchLog",
    "PayoffMatrix",
    "Noise",
    "RoundRobinTournament",
]
