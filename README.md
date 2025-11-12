# Iterated Prisoner's Dilemma Framework

A modular Python framework for simulating the Iterated Prisoner's Dilemma (IPD). This package provides classes to simulate matches, classic strategies, round-robin tournaments, and tools for analyzing and visualizing results.

## Requirements

- Python 3.10+
- `matplotlib>=3.7` for visualizations
- `numpy>=1.24` for array operations in heatmaps
- `pytest>=7.4` for running automated tests

## Installation

### Using pip

Install dependencies with:

```bash
pip install -r requirements.txt
```

### Using Conda

1. Make sure you have [Conda](https://docs.conda.io) installed (Miniconda or Anaconda).
2. Create a new environment with a supported Python version (>= 3.10). For example:
   ```bash
   conda create --name ipd-env python=3.11
   ```
3. Activate the newly created environment:
   ```bash
   conda activate ipd-env
   ```
4. Install project dependencies using `pip` with the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```
5. (Optional) Verify everything works by running the test suite:
   ```bash
   python -m pytest prisoners_dilemma/tests
   ```

**Note**: This project uses constructs introduced in Python 3.10; for this reason, the official CI covers Python 3.10 and 3.11.

## Quick Start

```python
from prisoners_dilemma.pd_core.player import Player
from prisoners_dilemma.pd_core.game import IteratedMatch
from prisoners_dilemma.strategies import TitForTat, AllDefect

match = IteratedMatch(
    Player(TitForTat()),
    Player(AllDefect()),
    n_rounds=100,
)
outcome, log = match.play()
print(outcome.mean_payoff_a, outcome.cooperation_rate_a)
```

## Example Scripts

The scripts in the `prisoners_dilemma/examples/` directory demonstrate how to use the framework:

- **`basic_match.py`**: Runs a noisy match between Tit For Tat and Always Defect with a round-by-round summary.
- **`simple_tournament.py`**: Runs a round-robin tournament between multiple strategies and prints the final leaderboard.
- **`tournament_with_plots.py`**: Runs a complete tournament with 8 strategies and generates visualizations (leaderboard, heatmaps, distributions, time series). Results are saved in `data/results/tournament_YYYYMMDD_HHMMSS/`.

Run the scripts directly or as Python modules:

```bash
python -m prisoners_dilemma.examples.basic_match
python -m prisoners_dilemma.examples.simple_tournament
python -m prisoners_dilemma.examples.tournament_with_plots
```

## Testing

Run the test suite with:

```bash
pytest prisoners_dilemma/tests
```

## Project Structure

```
prisoners_dilemma/
├─ pd_core/          # Core game logic, tournaments, metrics
├─ strategies/       # Strategy implementations
├─ visuals/          # Plotting and visualization tools
├─ experiments/      # Experiment configuration and analysis
├─ examples/         # Example scripts
└─ tests/           # Test suite
```

## Documentation

For detailed design guidelines and architecture documentation, see [`agents.md`](agents.md).

## Development Note

This project was developed as an experiment in LLM-assisted coding. The initial design and architecture were outlined in [`agents.md`](agents.md), which served as the blueprint for the entire framework. Subsequent development was carried out using AI coding assistants (Codex/GPT) based on that architectural specification.

The code has been reviewed and tested, and all components follow the project's quality standards as validated through the test suite. This project serves as both a functional IPD framework and a demonstration of structured LLM-assisted software development.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
