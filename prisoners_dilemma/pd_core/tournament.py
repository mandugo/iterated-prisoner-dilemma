"""Implementations of tournaments between strategies."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Iterable, Optional, Sequence

from .game import IteratedMatch, MatchOutcome, PayoffMatrix
from .noise import Noise
from .player import Player


@dataclass
class MatchSummary:
    player_a: str
    player_b: str
    outcome: MatchOutcome


@dataclass
class TournamentResults:
    matches: list[MatchSummary]

    def leaderboard(self) -> dict[str, float]:
        scores: dict[str, float] = {}
        for summary in self.matches:
            scores.setdefault(summary.player_a, 0.0)
            scores.setdefault(summary.player_b, 0.0)
            scores[summary.player_a] += summary.outcome.mean_payoff_a
            scores[summary.player_b] += summary.outcome.mean_payoff_b
        return scores


class RoundRobinTournament:
    """Round-robin tournament running a match for each pair of players."""

    def __init__(
        self,
        players: Sequence[Player],
        *,
        payoff_matrix: Optional[PayoffMatrix] = None,
        noise: Optional[Noise] = None,
        n_rounds: int = 200,
        repetitions: int = 1,
        seed: Optional[int] = None,
    ) -> None:
        if repetitions < 1:
            raise ValueError("repetitions must be >= 1")
        self.players = players
        self.payoff_matrix = payoff_matrix or PayoffMatrix()
        self.noise = noise
        self.n_rounds = n_rounds
        self.repetitions = repetitions
        self.seed = seed

    def run(self) -> TournamentResults:
        matches: list[MatchSummary] = []
        for player_a, player_b in combinations(self.players, 2):
            for rep in range(self.repetitions):
                match = IteratedMatch(
                    player_a,
                    player_b,
                    payoff_matrix=self.payoff_matrix,
                    noise=self.noise,
                    n_rounds=self.n_rounds,
                    seed=None if self.seed is None else self.seed + rep,
                )
                outcome, _ = match.play()
                matches.append(
                    MatchSummary(
                        player_a=player_a.display_name,
                        player_b=player_b.display_name,
                        outcome=outcome,
                    )
                )
        return TournamentResults(matches)
