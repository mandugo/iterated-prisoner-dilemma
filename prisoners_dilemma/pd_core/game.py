"""Game logic for the (Iterated) Prisoner's Dilemma."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional
import random

from .noise import Noise
from .strategy import Action, Strategy
from .player import Player
from .utils import make_rng


ACTIONS = ("C", "D")


@dataclass(frozen=True)
class PayoffMatrix:
    """Payoff matrix for a symmetric Prisoner's Dilemma."""

    temptation: float = 5.0
    reward: float = 3.0
    punishment: float = 1.0
    sucker: float = 0.0

    def payoff(self, a: Action, b: Action) -> tuple[float, float]:
        if a not in ACTIONS or b not in ACTIONS:
            raise ValueError("Actions must be 'C' or 'D'")
        if a == "C" and b == "C":
            return self.reward, self.reward
        if a == "C" and b == "D":
            return self.sucker, self.temptation
        if a == "D" and b == "C":
            return self.temptation, self.sucker
        return self.punishment, self.punishment


@dataclass(slots=True)
class MatchLog:
    actions_a: list[Action]
    actions_b: list[Action]
    payoff_a: list[float]
    payoff_b: list[float]

    def append(self, a: Action, b: Action, pa: float, pb: float) -> None:
        self.actions_a.append(a)
        self.actions_b.append(b)
        self.payoff_a.append(pa)
        self.payoff_b.append(pb)

    def as_rows(self) -> Iterable[tuple[int, Action, Action, float, float]]:
        for idx, (a, b, pa, pb) in enumerate(
            zip(self.actions_a, self.actions_b, self.payoff_a, self.payoff_b)
        ):
            yield idx, a, b, pa, pb

    @property
    def rounds(self) -> int:
        return len(self.actions_a)

    def cooperation_rate_a(self) -> float:
        return self.actions_a.count("C") / self.rounds if self.rounds else 0.0

    def cooperation_rate_b(self) -> float:
        return self.actions_b.count("C") / self.rounds if self.rounds else 0.0


@dataclass(frozen=True)
class MatchOutcome:
    total_payoff_a: float
    total_payoff_b: float
    mean_payoff_a: float
    mean_payoff_b: float
    cooperation_rate_a: float
    cooperation_rate_b: float


class IteratedMatch:
    """Simulate an iterated match between two players."""

    def __init__(
        self,
        player_a: Player,
        player_b: Player,
        *,
        payoff_matrix: Optional[PayoffMatrix] = None,
        noise: Optional[Noise] = None,
        n_rounds: Optional[int] = 200,
        continuation_prob: Optional[float] = None,
        seed: Optional[int] = None,
    ) -> None:
        if continuation_prob is not None and not (0 <= continuation_prob < 1):
            raise ValueError("continuation_prob must be in [0, 1)")
        if n_rounds is None and continuation_prob is None:
            raise ValueError("either n_rounds or continuation_prob must be provided")

        self.player_a = player_a
        self.player_b = player_b
        self.payoff_matrix = payoff_matrix or PayoffMatrix()
        self.noise = noise
        self.n_rounds = n_rounds
        self.continuation_prob = continuation_prob
        self._rng = make_rng(seed)

    def play(self) -> tuple[MatchOutcome, MatchLog]:
        log = MatchLog([], [], [], [])

        self.player_a.reset()
        self.player_b.reset()

        a_prev: Optional[Action] = None
        b_prev: Optional[Action] = None
        round_index = 0
        while self._continue(round_index):
            if round_index == 0:
                a_action = self.player_a.first_move()
                b_action = self.player_b.first_move()
            else:
                a_action = self.player_a.next_move(a_prev, b_prev)  # type: ignore[arg-type]
                b_action = self.player_b.next_move(b_prev, a_prev)  # type: ignore[arg-type]

            a_eff = self._apply_noise(a_action)
            b_eff = self._apply_noise(b_action)
            payoff_a, payoff_b = self.payoff_matrix.payoff(a_eff, b_eff)
            log.append(a_eff, b_eff, payoff_a, payoff_b)
            a_prev, b_prev = a_eff, b_eff
            round_index += 1

        outcome = self._build_outcome(log)
        return outcome, log

    def _continue(self, round_index: int) -> bool:
        if self.n_rounds is not None and round_index >= self.n_rounds:
            return False
        if round_index == 0:
            return True
        if self.continuation_prob is None:
            return round_index < (self.n_rounds or 0)
        return self._rng.random() < self.continuation_prob

    def _apply_noise(self, action: Action) -> Action:
        if self.noise is None:
            return action
        return self.noise.apply(action, self._rng)

    def _build_outcome(self, log: MatchLog) -> MatchOutcome:
        total_payoff_a = sum(log.payoff_a)
        total_payoff_b = sum(log.payoff_b)
        rounds = log.rounds or 1
        return MatchOutcome(
            total_payoff_a=total_payoff_a,
            total_payoff_b=total_payoff_b,
            mean_payoff_a=total_payoff_a / rounds,
            mean_payoff_b=total_payoff_b / rounds,
            cooperation_rate_a=log.cooperation_rate_a(),
            cooperation_rate_b=log.cooperation_rate_b(),
        )
