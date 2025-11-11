"""Command line interface to run predefined experiments.

The CLI expects a YAML configuration describing the roster of strategies
and tournament parameters.  The goal is to keep experiments reproducible
and easy to version-control.
"""

from __future__ import annotations

import argparse
import importlib
import json
from pathlib import Path
from typing import Any

import yaml

from ..pd_core.player import Player
from ..pd_core.tournament import RoundRobinTournament


def _load_strategy(path: str, params: dict[str, Any]) -> Any:
    module_name, class_name = path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    cls = getattr(module, class_name)
    return cls(**params)


def run_from_config(config: dict[str, Any]) -> dict[str, Any]:
    strategies = [
        Player(
            _load_strategy(entry["strategy"], entry.get("params", {})),
            name=entry.get("name"),
            seed=entry.get("seed"),
        )
        for entry in config["players"]
    ]

    tournament = RoundRobinTournament(
        strategies,
        n_rounds=config.get("n_rounds", 200),
        repetitions=config.get("repetitions", 1),
    )
    results = tournament.run()
    leaderboard = results.leaderboard()
    return {
        "matches": [
            {
                "player_a": match.player_a,
                "player_b": match.player_b,
                "mean_payoff_a": match.outcome.mean_payoff_a,
                "mean_payoff_b": match.outcome.mean_payoff_b,
                "cooperation_rate_a": match.outcome.cooperation_rate_a,
                "cooperation_rate_b": match.outcome.cooperation_rate_b,
            }
            for match in results.matches
        ],
        "leaderboard": leaderboard,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Iterated Prisoner's Dilemma experiments")
    parser.add_argument("config", type=Path, help="Path to a YAML configuration file")
    parser.add_argument("--output", type=Path, help="Optional path to save a JSON summary")
    args = parser.parse_args(argv)

    config = yaml.safe_load(args.config.read_text())
    summary = run_from_config(config)

    if args.output:
        args.output.write_text(json.dumps(summary, indent=2))
    else:
        print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
