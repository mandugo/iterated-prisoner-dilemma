"""High level plotting helpers using matplotlib."""

from __future__ import annotations

from collections import defaultdict
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np

from ..pd_core.game import MatchLog
from ..pd_core.tournament import TournamentResults


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


def plot_leaderboard(leaderboard: dict[str, float]) -> plt.Figure:
    """Create a horizontal bar chart showing tournament leaderboard.

    Parameters
    ----------
    leaderboard:
        Dictionary mapping strategy names to their cumulative mean payoff scores.

    Returns
    -------
    matplotlib.figure.Figure
        Figure containing the leaderboard bar chart.
    """
    sorted_items = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
    strategies = [item[0] for item in sorted_items]
    scores = [item[1] for item in sorted_items]

    fig, ax = plt.subplots(figsize=(10, max(6, len(strategies) * 0.5)))
    y_pos = np.arange(len(strategies))
    ax.barh(y_pos, scores)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(strategies)
    ax.set_xlabel("Cumulative Mean Payoff")
    ax.set_title("Tournament Leaderboard")
    ax.grid(True, alpha=0.3, axis="x")
    fig.tight_layout()
    return fig


def plot_payoff_heatmap(results: TournamentResults) -> plt.Figure:
    """Create a heatmap showing mean payoffs for each strategy matchup.

    Parameters
    ----------
    results:
        Tournament results containing all match outcomes.

    Returns
    -------
    matplotlib.figure.Figure
        Figure containing the payoff heatmap.
    """
    # Collect all unique strategy names
    strategies = sorted(set(sum([[m.player_a, m.player_b] for m in results.matches], [])))

    # Build payoff matrix: [strategy_a][strategy_b] -> list of payoffs
    payoff_data: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))

    for match in results.matches:
        payoff_data[match.player_a][match.player_b].append(match.outcome.mean_payoff_a)
        payoff_data[match.player_b][match.player_a].append(match.outcome.mean_payoff_b)

    # Create matrix with mean payoffs
    n = len(strategies)
    matrix = np.zeros((n, n))
    for i, strat_a in enumerate(strategies):
        for j, strat_b in enumerate(strategies):
            if strat_a == strat_b:
                # Self-match: use average of all matches for this strategy
                payoffs = []
                for other_strat in strategies:
                    if other_strat != strat_a:
                        payoffs.extend(payoff_data[strat_a].get(other_strat, []))
                matrix[i, j] = np.mean(payoffs) if payoffs else 0.0
            else:
                payoffs = payoff_data[strat_a].get(strat_b, [])
                matrix[i, j] = np.mean(payoffs) if payoffs else 0.0

    fig, ax = plt.subplots(figsize=(max(8, n * 0.8), max(8, n * 0.8)))
    im = ax.imshow(matrix, cmap="RdYlGn", aspect="auto")
    ax.set_xticks(np.arange(n))
    ax.set_yticks(np.arange(n))
    ax.set_xticklabels(strategies, rotation=45, ha="right")
    ax.set_yticklabels(strategies)
    ax.set_xlabel("Opponent Strategy")
    ax.set_ylabel("Strategy")
    ax.set_title("Mean Payoff Heatmap (Strategy vs Opponent)")

    # Add text annotations
    for i in range(n):
        for j in range(n):
            text = ax.text(j, i, f"{matrix[i, j]:.1f}", ha="center", va="center", color="black", fontsize=8)

    plt.colorbar(im, ax=ax, label="Mean Payoff")
    fig.tight_layout()
    return fig


def plot_cooperation_heatmap(results: TournamentResults) -> plt.Figure:
    """Create a heatmap showing cooperation rates for each strategy matchup.

    Parameters
    ----------
    results:
        Tournament results containing all match outcomes.

    Returns
    -------
    matplotlib.figure.Figure
        Figure containing the cooperation rate heatmap.
    """
    # Collect all unique strategy names
    strategies = sorted(set(sum([[m.player_a, m.player_b] for m in results.matches], [])))

    # Build cooperation matrix: [strategy_a][strategy_b] -> list of cooperation rates
    coop_data: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))

    for match in results.matches:
        coop_data[match.player_a][match.player_b].append(match.outcome.cooperation_rate_a)
        coop_data[match.player_b][match.player_a].append(match.outcome.cooperation_rate_b)

    # Create matrix with mean cooperation rates
    n = len(strategies)
    matrix = np.zeros((n, n))
    for i, strat_a in enumerate(strategies):
        for j, strat_b in enumerate(strategies):
            if strat_a == strat_b:
                # Self-match: use average of all matches for this strategy
                rates = []
                for other_strat in strategies:
                    if other_strat != strat_a:
                        rates.extend(coop_data[strat_a].get(other_strat, []))
                matrix[i, j] = np.mean(rates) if rates else 0.0
            else:
                rates = coop_data[strat_a].get(strat_b, [])
                matrix[i, j] = np.mean(rates) if rates else 0.0

    fig, ax = plt.subplots(figsize=(max(8, n * 0.8), max(8, n * 0.8)))
    im = ax.imshow(matrix, cmap="Blues", aspect="auto", vmin=0.0, vmax=1.0)
    ax.set_xticks(np.arange(n))
    ax.set_yticks(np.arange(n))
    ax.set_xticklabels(strategies, rotation=45, ha="right")
    ax.set_yticklabels(strategies)
    ax.set_xlabel("Opponent Strategy")
    ax.set_ylabel("Strategy")
    ax.set_title("Cooperation Rate Heatmap (Strategy vs Opponent)")

    # Add text annotations
    for i in range(n):
        for j in range(n):
            text = ax.text(j, i, f"{matrix[i, j]:.2f}", ha="center", va="center", color="white" if matrix[i, j] > 0.5 else "black", fontsize=8)

    plt.colorbar(im, ax=ax, label="Cooperation Rate")
    fig.tight_layout()
    return fig


def plot_payoff_distribution(results: TournamentResults) -> plt.Figure:
    """Create a box plot showing payoff distribution per strategy.

    Parameters
    ----------
    results:
        Tournament results containing all match outcomes.

    Returns
    -------
    matplotlib.figure.Figure
        Figure containing the payoff distribution plot.
    """
    # Collect payoffs per strategy
    strategy_payoffs: dict[str, list[float]] = defaultdict(list)

    for match in results.matches:
        strategy_payoffs[match.player_a].append(match.outcome.mean_payoff_a)
        strategy_payoffs[match.player_b].append(match.outcome.mean_payoff_b)

    # Prepare data for box plot
    strategies = sorted(strategy_payoffs.keys())
    payoffs_list = [strategy_payoffs[strat] for strat in strategies]

    fig, ax = plt.subplots(figsize=(max(10, len(strategies) * 0.8), 6))
    bp = ax.boxplot(payoffs_list, labels=strategies, patch_artist=True)

    # Color the boxes
    colors = plt.cm.Set3(np.linspace(0, 1, len(bp["boxes"])))
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    ax.set_ylabel("Mean Payoff per Match")
    ax.set_xlabel("Strategy")
    ax.set_title("Payoff Distribution by Strategy")
    ax.grid(True, alpha=0.3, axis="y")
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    return fig


def plot_match_timeseries(log: MatchLog, player_a_name: str, player_b_name: str) -> plt.Figure:
    """Create a time series plot showing cooperation rates and cumulative payoffs over rounds.

    Parameters
    ----------
    log:
        Match log containing actions and payoffs for each round.
    player_a_name:
        Display name for player A.
    player_b_name:
        Display name for player B.

    Returns
    -------
    matplotlib.figure.Figure
        Figure containing the time series plot.
    """
    rounds = range(1, log.rounds + 1)

    # Calculate cumulative cooperation rates
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

    # Calculate cumulative payoffs
    cumulative_payoff_a = []
    cumulative_payoff_b = []
    payoff_a_sum = 0.0
    payoff_b_sum = 0.0
    for pa, pb in zip(log.payoff_a, log.payoff_b):
        payoff_a_sum += pa
        payoff_b_sum += pb
        cumulative_payoff_a.append(payoff_a_sum)
        cumulative_payoff_b.append(payoff_b_sum)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # Plot cooperation rates
    ax1.plot(rounds, cumulative_coop_a, label=player_a_name, linewidth=2)
    ax1.plot(rounds, cumulative_coop_b, label=player_b_name, linewidth=2)
    ax1.set_ylabel("Cooperation Rate")
    ax1.set_title(f"Match Time Series: {player_a_name} vs {player_b_name}")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 1)

    # Plot cumulative payoffs
    ax2.plot(rounds, cumulative_payoff_a, label=player_a_name, linewidth=2)
    ax2.plot(rounds, cumulative_payoff_b, label=player_b_name, linewidth=2)
    ax2.set_xlabel("Round")
    ax2.set_ylabel("Cumulative Payoff")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    fig.tight_layout()
    return fig
