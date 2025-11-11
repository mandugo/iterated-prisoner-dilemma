"""High level plotting helpers using matplotlib."""

from __future__ import annotations

from typing import Iterable

import matplotlib.pyplot as plt

from ..pd_core.game import MatchLog


def cooperation_curve(log: MatchLog) -> plt.Figure:
    rounds = range(1, log.rounds + 1)
    cumulative_coop_a = []
    cumulative_coop_b = []
    coop_a = 0
    coop_b = 0
    for idx, (a_action, b_action) in enumerate(zip(log.actions_a, log.actions_b), start=1):
        if a_action == "C":
            coop_a += 1
        if b_action == "C":
            coop_b += 1
        cumulative_coop_a.append(coop_a / idx)
        cumulative_coop_b.append(coop_b / idx)

    fig, ax = plt.subplots()
    ax.plot(rounds, cumulative_coop_a, label="Player A")
    ax.plot(rounds, cumulative_coop_b, label="Player B")
    ax.set_xlabel("Round")
    ax.set_ylabel("Cooperation rate")
    ax.legend()
    ax.grid(True, alpha=0.3)
    return fig
