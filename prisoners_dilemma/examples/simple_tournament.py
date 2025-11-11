"""Run a tiny round-robin tournament among built-in strategies."""

from __future__ import annotations

from prisoners_dilemma.pd_core.player import Player
from prisoners_dilemma.pd_core.tournament import RoundRobinTournament
from prisoners_dilemma.strategies.probabilistic import GenerousTitForTat, RandomStrategy
from prisoners_dilemma.strategies.simple import AllCooperate, AllDefect, Pavlov, TitForTat


def main() -> None:
    """Execute the tournament and print a leaderboard."""

    roster = [
        Player(AllCooperate(), name="ALLC"),
        Player(AllDefect(), name="ALLD"),
        Player(TitForTat(), name="TFT"),
        Player(Pavlov(), name="PAVLOV"),
        Player(RandomStrategy(p=0.3), name="RAND(0.3)", seed=5),
        Player(GenerousTitForTat(forgive_p=0.2), name="GTFT(0.2)", seed=9),
    ]

    tournament = RoundRobinTournament(
        roster,
        n_rounds=100,
        repetitions=3,
        seed=2024,
    )

    results = tournament.run()
    leaderboard = results.leaderboard()

    print("Round-robin tournament (100 rounds, 3 repetitions)")
    print("=" * 54)
    for name, score in sorted(leaderboard.items(), key=lambda item: item[1], reverse=True):
        print(f"{name:10s} -> cumulative mean payoff {score:.2f}")

    print("\nIndividual match outcomes:")
    for summary in results.matches:
        outcome = summary.outcome
        print(
            f"{summary.player_a:10s} vs {summary.player_b:10s} | "
            f"mean payoff {outcome.mean_payoff_a:.2f} vs {outcome.mean_payoff_b:.2f}"
        )


if __name__ == "__main__":
    main()
