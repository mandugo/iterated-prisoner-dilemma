"""Run a single iterated match between two classic strategies."""

from __future__ import annotations

from prisoners_dilemma.pd_core.game import IteratedMatch, PayoffMatrix
from prisoners_dilemma.pd_core.noise import Noise
from prisoners_dilemma.pd_core.player import Player
from prisoners_dilemma.strategies.simple import AllDefect, TitForTat


def main() -> None:
    """Execute a short noisy match and print a human-friendly summary."""

    player_a = Player(TitForTat(), name="Tit For Tat", seed=7)
    player_b = Player(AllDefect(), name="Always Defect", seed=21)

    match = IteratedMatch(
        player_a,
        player_b,
        payoff_matrix=PayoffMatrix(),
        noise=Noise(epsilon=0.05),
        n_rounds=10,
        seed=1234,
    )

    outcome, log = match.play()

    print("Tit For Tat vs Always Defect (10 rounds, epsilon=0.05)")
    print("=" * 54)
    for round_idx, action_a, action_b, payoff_a, payoff_b in log.as_rows():
        print(
            f"Round {round_idx + 1:02d}: {player_a.display_name} -> {action_a} "
            f"(payoff {payoff_a:.0f}) | "
            f"{player_b.display_name} -> {action_b} (payoff {payoff_b:.0f})"
        )

    print("-" * 54)
    print(
        f"Totals: {player_a.display_name} {outcome.total_payoff_a:.1f} "
        f"vs {player_b.display_name} {outcome.total_payoff_b:.1f}"
    )
    print(
        f"Cooperation rates: {player_a.display_name} {outcome.cooperation_rate_a:.2%}, "
        f"{player_b.display_name} {outcome.cooperation_rate_b:.2%}"
    )


if __name__ == "__main__":
    main()
