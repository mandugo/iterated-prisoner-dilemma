"""Evolutionary population dynamics utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


def replicator_step(population: Mapping[str, float], fitness: Mapping[str, float]) -> dict[str, float]:
    """Return the updated population after one discrete replicator step."""

    total_fitness = sum(population[name] * fitness.get(name, 0.0) for name in population)
    if total_fitness == 0:
        return dict(population)
    next_population: dict[str, float] = {}
    for name, proportion in population.items():
        fit = fitness.get(name, 0.0)
        next_population[name] = proportion * fit / total_fitness
    return next_population
