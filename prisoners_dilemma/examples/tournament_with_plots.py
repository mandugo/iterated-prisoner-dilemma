"""Run a comprehensive tournament with multiple strategies and generate visual insights."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt

from prisoners_dilemma.pd_core.game import IteratedMatch, PayoffMatrix
from prisoners_dilemma.pd_core.noise import Noise
from prisoners_dilemma.pd_core.player import Player
from prisoners_dilemma.pd_core.tournament import RoundRobinTournament
from prisoners_dilemma.strategies.probabilistic import GenerousTitForTat, RandomStrategy
from prisoners_dilemma.strategies.simple import (
    AllCooperate,
    AllDefect,
    GrimTrigger,
    Pavlov,
    TitForTat,
    TitForTwoTats,
)
from prisoners_dilemma.visuals.plots import (
    plot_cooperation_heatmap,
    plot_leaderboard,
    plot_match_timeseries,
    plot_payoff_distribution,
    plot_payoff_heatmap,
)
from prisoners_dilemma.visuals.styles import apply_default_style


def main() -> None:
    """Execute tournament, generate visualizations, and save outputs."""
    # Apply default matplotlib style
    apply_default_style()

    # Setup tournament parameters
    n_rounds = 200
    repetitions = 5
    noise = Noise(epsilon=0.02)
    seed = 2024

    # Create diverse roster of strategies
    roster = [
        Player(AllCooperate(), name="ALLC"),
        Player(AllDefect(), name="ALLD"),
        Player(TitForTat(), name="TFT"),
        Player(TitForTwoTats(), name="TF2T"),
        Player(GrimTrigger(), name="GRIM"),
        Player(Pavlov(), name="PAVLOV"),
        Player(GenerousTitForTat(forgive_p=0.2), name="GTFT(0.2)", seed=9),
        Player(RandomStrategy(p=0.3), name="RAND(0.3)", seed=5),
    ]

    print("=" * 70)
    print("Iterated Prisoner's Dilemma Tournament")
    print("=" * 70)
    print(f"Strategies: {len(roster)}")
    print(f"Rounds per match: {n_rounds}")
    print(f"Repetitions: {repetitions}")
    print(f"Noise (epsilon): {noise.epsilon}")
    print(f"Seed: {seed}")
    print("=" * 70)
    print("\nRunning tournament...")

    # Run tournament
    tournament = RoundRobinTournament(
        roster,
        n_rounds=n_rounds,
        repetitions=repetitions,
        noise=noise,
        seed=seed,
    )

    results = tournament.run()
    leaderboard = results.leaderboard()

    print(f"Tournament completed! Total matches: {len(results.matches)}")
    print("\nLeaderboard:")
    print("-" * 70)
    for rank, (name, score) in enumerate(
        sorted(leaderboard.items(), key=lambda item: item[1], reverse=True), start=1
    ):
        print(f"{rank:2d}. {name:15s} -> {score:8.2f}")

    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path("data") / "results" / f"tournament_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nGenerating visualizations...")
    print(f"Output directory: {output_dir}")

    # Generate and save visualizations
    print("  - Leaderboard bar chart...")
    fig_leaderboard = plot_leaderboard(leaderboard)
    fig_leaderboard.savefig(output_dir / "leaderboard.png", dpi=150, bbox_inches="tight")
    plt.close(fig_leaderboard)

    print("  - Payoff heatmap...")
    fig_payoff_heatmap = plot_payoff_heatmap(results)
    fig_payoff_heatmap.savefig(output_dir / "payoff_heatmap.png", dpi=150, bbox_inches="tight")
    plt.close(fig_payoff_heatmap)

    print("  - Cooperation rate heatmap...")
    fig_coop_heatmap = plot_cooperation_heatmap(results)
    fig_coop_heatmap.savefig(output_dir / "cooperation_heatmap.png", dpi=150, bbox_inches="tight")
    plt.close(fig_coop_heatmap)

    print("  - Payoff distribution...")
    fig_distribution = plot_payoff_distribution(results)
    fig_distribution.savefig(output_dir / "payoff_distribution.png", dpi=150, bbox_inches="tight")
    plt.close(fig_distribution)

    # Generate time series for interesting matchups
    print("  - Match time series...")
    interesting_matchups = [
        ("TFT", "GRIM"),
        ("PAVLOV", "GTFT(0.2)"),
        ("TFT", "ALLD"),
    ]

    payoff_matrix = PayoffMatrix()
    for strat_a_name, strat_b_name in interesting_matchups:
        # Find players by name
        player_a = next(p for p in roster if p.display_name == strat_a_name)
        player_b = next(p for p in roster if p.display_name == strat_b_name)

        # Run a match to get the log
        match = IteratedMatch(
            player_a,
            player_b,
            payoff_matrix=payoff_matrix,
            noise=noise,
            n_rounds=n_rounds,
            seed=seed,
        )
        outcome, log = match.play()

        # Generate time series plot
        fig_timeseries = plot_match_timeseries(log, player_a.display_name, player_b.display_name)
        filename = f"match_timeseries_{strat_a_name}_vs_{strat_b_name}.png"
        # Replace characters that might cause issues in filenames
        filename = filename.replace("(", "").replace(")", "").replace(".", "_")
        fig_timeseries.savefig(output_dir / filename, dpi=150, bbox_inches="tight")
        plt.close(fig_timeseries)

    # Save summary statistics to text file
    summary_file = output_dir / "summary.txt"
    with open(summary_file, "w") as f:
        f.write("Tournament Summary\n")
        f.write("=" * 70 + "\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Strategies: {len(roster)}\n")
        f.write(f"Rounds per match: {n_rounds}\n")
        f.write(f"Repetitions: {repetitions}\n")
        f.write(f"Noise (epsilon): {noise.epsilon}\n")
        f.write(f"Seed: {seed}\n")
        f.write(f"Total matches: {len(results.matches)}\n")
        f.write("\nLeaderboard:\n")
        f.write("-" * 70 + "\n")
        for rank, (name, score) in enumerate(
            sorted(leaderboard.items(), key=lambda item: item[1], reverse=True), start=1
        ):
            f.write(f"{rank:2d}. {name:15s} -> {score:8.2f}\n")

    print(f"\nAll visualizations saved to: {output_dir}")
    print("Summary statistics saved to: summary.txt")


if __name__ == "__main__":
    main()

