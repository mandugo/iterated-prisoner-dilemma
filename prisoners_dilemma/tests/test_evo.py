from prisoners_dilemma.pd_core.evo import replicator_step


def test_replicator_step_normalized() -> None:
    population = {"A": 0.5, "B": 0.5}
    fitness = {"A": 2.0, "B": 1.0}
    next_pop = replicator_step(population, fitness)
    assert next_pop["A"] > next_pop["B"]
    assert abs(sum(next_pop.values()) - 1.0) < 1e-6


def test_replicator_step_zero_total() -> None:
    population = {"A": 0.7, "B": 0.3}
    fitness = {"A": 0.0, "B": 0.0}
    assert replicator_step(population, fitness) == population
