import random

import pytest

from prisoners_dilemma.pd_core.game import IteratedMatch, PayoffMatrix
from prisoners_dilemma.pd_core.noise import Noise
from prisoners_dilemma.pd_core.player import Player
from prisoners_dilemma.strategies import AllCooperate, AllDefect, TitForTat


def test_payoff_matrix_default_ordering() -> None:
    matrix = PayoffMatrix()
    assert matrix.payoff("C", "C") == (matrix.reward, matrix.reward)
    assert matrix.payoff("C", "D") == (matrix.sucker, matrix.temptation)
    assert matrix.payoff("D", "C") == (matrix.temptation, matrix.sucker)
    assert matrix.payoff("D", "D") == (matrix.punishment, matrix.punishment)


def test_iterated_match_basic() -> None:
    match = IteratedMatch(Player(AllCooperate()), Player(AllDefect()), n_rounds=3)
    outcome, log = match.play()
    assert log.rounds == 3
    assert outcome.total_payoff_a == pytest.approx(0.0)
    assert outcome.total_payoff_b == pytest.approx(15.0)
    assert outcome.cooperation_rate_a == pytest.approx(1.0)
    assert outcome.cooperation_rate_b == pytest.approx(0.0)


def test_noise_flip_probability() -> None:
    noise = Noise(epsilon=1.0)
    rng = random.Random(0)
    assert noise.apply("C", rng) == "D"
    assert noise.apply("D", rng) == "C"


def test_continuation_probability() -> None:
    match = IteratedMatch(
        Player(TitForTat()),
        Player(TitForTat()),
        n_rounds=None,
        continuation_prob=0.0,
    )
    outcome, log = match.play()
    assert log.rounds == 1
    assert outcome.mean_payoff_a == pytest.approx(outcome.mean_payoff_b)
