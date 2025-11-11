import random

from prisoners_dilemma.strategies import (
    AllCooperate,
    AllDefect,
    GenerousTitForTat,
    GrimTrigger,
    Pavlov,
    RandomStrategy,
    TitForTat,
    TitForTwoTats,
)


def test_allc_always_cooperates() -> None:
    strat = AllCooperate()
    rng = random.Random(0)
    assert strat.first_move(rng) == "C"
    assert strat.next_move("C", "D", rng) == "C"


def test_alld_always_defects() -> None:
    strat = AllDefect()
    rng = random.Random(0)
    assert strat.first_move(rng) == "D"
    assert strat.next_move("C", "C", rng) == "D"


def test_tft_mirrors_opponent() -> None:
    strat = TitForTat()
    rng = random.Random(0)
    assert strat.first_move(rng) == "C"
    assert strat.next_move("C", "D", rng) == "D"


def test_tf2t_requires_two_defections() -> None:
    strat = TitForTwoTats()
    rng = random.Random(0)
    assert strat.first_move(rng) == "C"
    assert strat.next_move("C", "D", rng) == "C"
    assert strat.next_move("C", "D", rng) == "D"


def test_grim_trigger_never_forgives() -> None:
    strat = GrimTrigger()
    rng = random.Random(0)
    strat.first_move(rng)
    strat.next_move("C", "D", rng)
    assert strat.next_move("D", "C", rng) == "D"


def test_pavlov_win_stay_lose_shift() -> None:
    strat = Pavlov()
    rng = random.Random(0)
    assert strat.first_move(rng) == "C"
    assert strat.next_move("C", "C", rng) == "C"
    assert strat.next_move("C", "D", rng) == "D"


def test_random_strategy_bounds() -> None:
    strat = RandomStrategy(p=1.0)
    rng = random.Random(0)
    assert strat.first_move(rng) == "C"
    strat = RandomStrategy(p=0.0)
    assert strat.first_move(rng) == "D"


def test_generous_tft_forgives() -> None:
    strat = GenerousTitForTat(forgive_p=1.0)
    rng = random.Random(0)
    strat.first_move(rng)
    assert strat.next_move("C", "D", rng) == "C"
