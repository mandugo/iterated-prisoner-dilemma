# Complete Guide for Designing and Simulating the (Iterated) Prisoner's Dilemma in Python

**Objective**: Design a modular and testable Python framework to simulate Prisoner's Dilemma (PD) and Iterated Prisoner's Dilemma (IPD), run tournaments between strategies, analyze results, and visualize behaviors.

---

## 1. Requirements and Scope

### Functional Requirements

- Simulate single matches (one-shot PD) and repeated matches (IPD) with fixed or random number of rounds (geometrically terminating).
- Handle noise/action errors (e.g., flip an action with probability epsilon).
- Define an extensible set of strategies via common interface/abstraction.
- Execute 1-vs-1 matches, all-play-all tournaments, round-robin tournaments, and evolutionary populations (replicator dynamics).
- Calculate and save metrics (mean payoff, cooperation rate, run lengths, state transitions, scores per round, etc.).
- Provide visualizations (time series, distributions, payoff matrices, cooperation heatmaps, state diagrams, evolutionary dynamics).
- Reproducibility: random seeds, versioned configurations (YAML/JSON), logging.

### Non-Functional Requirements

- Clean, typed code (type hints), easy to test (pytest), documented (docstrings + README/agents.md).
- Python package structure with clear separation between core, strategies, experiment execution, and plotting.
- Performance: avoid bottlenecks (use numpy where useful), optional parallelization (multiprocessing) for large tournaments.

---

## 2. Project Structure

```text
prisoners_dilemma/
├─ pd_core/
│  ├─ __init__.py
│  ├─ game.py              # PD/IPD logic, PayoffMatrix, Match, Series
│  ├─ strategy.py          # Strategy interface, common utilities for state memory
│  ├─ player.py            # Agent/Player wrapper (strategy + state)
│  ├─ tournament.py        # round-robin, all-play-all, championships, bracket
│  ├─ evo.py               # evolutionary dynamics (replicator, mutation)
│  ├─ metrics.py           # metric collection/aggregation
│  ├─ noise.py             # noise models (flip, imperfect observation)
│  └─ utils.py             # RNG, seed, helpers
│
├─ strategies/
│  ├─ __init__.py
│  ├─ base.py              # base/common primitive classes
│  ├─ simple.py            # ALLC, ALLD, TFT, TF2T, Grim, Pavlov
│  ├─ probabilistic.py    # Random(p), GenerousTFT, smooth strategies
│  ├─ memory.py           # longer memories, noise correctors
│  ├─ zd.py               # Zero-Determinant (optional advanced)
│  └─ ml.py               # adaptive/evolutionary strategies (placeholder)
│
├─ experiments/
│  ├─ configs/            # YAML experiment files (parameters, seed, roster)
│  ├─ run_experiment.py   # CLI entrypoint to run experiments
│  ├─ analyze_results.py  # analysis/plotting scripts
│  └─ notebooks/          # (optional) Jupyter explorations
│
├─ visuals/
│  ├─ plots.py            # high-level API for plots
│  └─ styles.py           # common aesthetic rules (without forcing colors)
│
├─ tests/
│  ├─ test_game.py
│  ├─ test_strategies.py
│  ├─ test_tournament.py
│  ├─ test_evo.py
│  └─ test_metrics.py
│
├─ data/
│  ├─ raw/
│  ├─ processed/
│  └─ results/
│
├─ README.md
└─ agents.md               # this guide file
```

---

## 3. Game Model

### 3.1 Choices and Payoffs

- **Actions**: C (Cooperate), D (Defect).
- **Standard payoffs**: T > R > P > S (e.g., T=5, R=3, P=1, S=0).
- **Payoff matrix** (for player A; B is symmetric):
  - (C,C) → R
  - (C,D) → S
  - (D,C) → T
  - (D,D) → P

The system must allow custom and versioned payoffs.

### 3.2 Noise (Noise Models)

- **Action flip**: With probability epsilon, the chosen action is inverted.
- **Observation noise** (optional): Each player observes the opponent's action with error.
- **Start noise**: Initial move randomized with bias.

### 3.3 IPD Game Horizon

- **Fixed**: n_rounds.
- **Stochastic**: Continuation with probability delta (equivalent to geometric discount).

---

## 4. Class Architecture

### 4.1 Strategy Interface

```python
class Strategy(Protocol):
    name: str
    def reset(self) -> None: ...
    def first_move(self, rng: random.Random) -> str: ...  # 'C' or 'D'
    def next_move(self, my_last: str | None, opp_last: str | None, rng: random.Random) -> str: ...
```

- **Stateless vs stateful**: Some strategies maintain memory (e.g., GRIM, PAVLOV). State must be reset with `reset()`.
- **Extended memory**: Provide mixin/utils to access outcome history if needed (list of tuples of moves or payoffs).
- **Parameters**: Each strategy must accept parameters in the constructor (e.g., p for Random, forgiveness probability for GTFT).

### 4.2 Player/Agent

```python
@dataclass
class Player:
    strategy: Strategy
    id: str | None = None
```

- Wrapper to track identity and strategy instance.

### 4.3 PayoffMatrix

```python
@dataclass(frozen=True)
class PayoffMatrix:
    R: int
    S: int
    T: int
    P: int
    def payoff(self, a: str, b: str) -> tuple[int, int]: ...
```

### 4.4 Match (one-shot) and Series (IPD)

```python
@dataclass
class MatchResult:
    actions: list[tuple[str, str]]
    payoffs: list[tuple[int, int]]
    cum_payoff: tuple[int, int]
    coop_rate: tuple[float, float]

class Game:
    def play_oneshot(self, A: Player, B: Player, matrix: PayoffMatrix, rng: Random, noise: Noise | None) -> MatchResult: ...

class IteratedGame:
    def play(self, A: Player, B: Player, matrix: PayoffMatrix, rng: Random, noise: Noise | None, n_rounds: int | None = None, delta: float | None = None) -> MatchResult: ...
```

- Collect telemetry per round (actions, payoffs, states) for fine-grained analysis.

### 4.5 Tournament API

```python
@dataclass
class TournamentConfig:
    roster: list[Player]             # or strategy factories
    matrix: PayoffMatrix
    n_rounds: int
    delta: float | None
    noise: Noise | None
    repetitions: int = 1            # repeat matches to average noise
    pairing: Literal['round_robin','all_play_all','double_rr'] = 'round_robin'
    parallel: bool = False
    seed: int | None = None

class Tournament:
    def run(self, cfg: TournamentConfig) -> TournamentResult: ...
```

### 4.6 Evolution (Optional but Recommended)

```python
@dataclass
class EvolutionConfig:
    strategies: list[type[Strategy]] | list[Callable[[], Strategy]]
    population: dict[str, int]            # per strategy → count
    fitness: Literal['mean_payoff','median','coop_rate'] = 'mean_payoff'
    mutation_rate: float = 0.0
    generations: int = 200
    tournament_cfg: TournamentConfig      # reuse IPD rules

class Evolution:
    def run(self, cfg: EvolutionConfig) -> EvolutionResult: ...
```

- **Replicator dynamics**: Proportion ∝ relative fitness; add mutation/rare invaders.

---

## 5. Strategies to Implement (MVP → Advanced)

### MVP (Solid Baselines)

1. **ALLC** (Always Cooperate)
2. **ALLD** (Always Defect)
3. **TFT** (Tit for Tat)
4. **TF2T** (Tit for Two Tats)
5. **GRIM** (Grim Trigger)
6. **PAVLOV** / Win-Stay, Lose-Shift
7. **RANDOM(p)** (Bernoulli mixed)
8. **GTFT** (Generous Tit for Tat; parameter `forgive_p`)

### Advanced (Noise/Memory)

1. **NoisyTFT** (single error corrector, memory 2–3)
2. **Adaptive** (estimate p(C|state) of opponent, myopic best response)

### Extra (Research)

1. **Zero-Determinant** (Press & Dyson; extortionate and generous)
2. **Evolutionary/ML** (genetic, Q-learning; placeholder with coherent interface)

Each strategy must define: `name`, parameters, `reset`, `first_move`, `next_move`, docstring with references.

---

## 6. Metrics and Logging

### Metrics for Match/Series

- Cumulative and mean payoff (per player and total).
- Cooperation rate per player and joint (fraction of C).
- State transitions: count of (CC, CD, DC, DD), 2×2 matrix.
- Streaks: run lengths of C/D.
- Stationarity: time to converge to recurring patterns.

### Tournament Metrics

- Ranking (mean and variance of payoff per strategy).
- Payoff matrix (row: strategy A; column: strategy B → mean payoff A vs B).
- Average cooperation per matchup.
- Noise robustness: curves varying epsilon/delta/n_rounds.

### Result Persistence

- Save to CSV/Parquet: `results/matches.csv`, `results/summary.csv`.
- Save config (YAML) and seed used for traceability.

---

## 7. Visualizations (Plots) — Guidelines

Visualizations are implemented with matplotlib, avoiding forced styles/colors a priori and cluttered graphs.

1. **Time series**: Payoff per round, cumulative cooperation, state (CC, CD, DC, DD) for a pair of strategies.
2. **Heatmap**: Mean payoff of A against B; average cooperation of A against B.
3. **Distributions**: Histograms/ECDF of mean payoffs per strategy (over repetitions).
4. **Noise curve**: Mean payoff vs epsilon; cooperation vs epsilon (multiple strategies on same figure separated).
5. **Evolutionary dynamics**: Simplex/line-chart of population frequencies over time (generations).
6. **State diagrams** (small): Transitions between CC, CD, DC, DD with proportional thickness (save as PNG/SVG).

Each graph must have: informative title, labeled axes, clear legend, minimal annotations for main insights.

---

## 8. Experiment Pipeline

### 8.1 Config YAML (Example)

```yaml
seed: 42
matrix: {R: 3, S: 0, T: 5, P: 1}
noise: {type: action_flip, epsilon: 0.02}
match:
  mode: ipd
  n_rounds: 200
  delta: null
repetitions: 20
roster:
  - {strategy: TFT}
  - {strategy: GRIM}
  - {strategy: PAVLOV}
  - {strategy: GTFT, params: {forgive_p: 0.1}}
  - {strategy: RANDOM, params: {p: 0.3}}
output_dir: data/results/exp001
```

### 8.2 Execution

```bash
python experiments/run_experiment.py --config experiments/configs/exp001.yaml
```

- CLI options: override `n_rounds`, `epsilon`, `repetitions`, `parallel`, `output_dir`.

### 8.3 Analysis

```bash
python experiments/analyze_results.py --input data/results/exp001
```

- Produces summary tables + plots in `data/results/exp001/plots/`.

---

## 9. Key Implementation Details

### 9.1 Noise

Implement Noise as callable:

```python
@dataclass
class Noise:
    epsilon: float = 0.0
    def apply(self, action: str, rng: Random) -> str:
        return action if rng.random() > self.epsilon else ('D' if action=='C' else 'C')
```

- Integrate into game loop immediately after action choice and before payoff.

### 9.2 IPD Loop (Draft)

```python
A.strategy.reset(); B.strategy.reset()
a_prev = b_prev = None
for t in range(n_rounds) or while rng.random() < delta:
    a = A.strategy.first_move(rng) if t == 0 else A.strategy.next_move(a_prev, b_prev, rng)
    b = B.strategy.first_move(rng) if t == 0 else B.strategy.next_move(b_prev, a_prev, rng)
    a_eff = noise.apply(a, rng) if noise else a
    b_eff = noise.apply(b, rng) if noise else b
    pa, pb = matrix.payoff(a_eff, b_eff)
    # log effective actions and payoffs; update prev
    a_prev, b_prev = a_eff, b_eff
```

### 9.3 Efficient Metrics

- Calculate on-the-fly: counters `nC_A`, `nC_B`, `cc`, `cd`, `dc`, `dd`, payoff sums.
- At the end, derive rates and averages.

### 9.4 Tournament Parallelization

- Use `multiprocessing.Pool` or `concurrent.futures.ProcessPoolExecutor` to parallelize matches.
- Pass derived seeds (e.g., `seed_base + hash(pairing)`) for independence.

### 9.5 Tests (pytest)

- **PayoffMatrix**: Consistency T>R>P>S; correct mapping.
- **Noise**: Flip frequency ≈ epsilon over large N.
- **Strategies**: Base cases (ALLC vs ALLD), reciprocal TFT, GRIM punishes.
- **Game**: Length conservation, expected cooperation rates.
- **Tournament**: Determinism for epsilon=0, repetitions=1, fixed seed.

---

## 10. Development Strategy (Roadmap)

1. **Minimal core**: PayoffMatrix, Strategy (protocol), Noise, Game/IteratedGame with minimal logging.
2. **MVP strategies**: ALLC, ALLD, TFT, GRIM, PAVLOV, TF2T, RANDOM(p), GTFT.
3. **Metrics**: Result objects and aggregation functions; CSV saving.
4. **Tournament**: Round-robin with repetitions; simple CLI.
5. **Visuals**: Time series, payoff heatmap, ranking bar chart.
6. **Advanced noise**: NoisyTFT, imperfect observation.
7. **Evolution**: Replicator + mutation; dynamics graphs.
8. **Optimizations**: Parallel, numpy, caching.
9. **QA**: Tests + docs; reproducible examples.

### "Done" Criteria for MVP

- Tournament between 6–8 strategies on 200 rounds × 20 repetitions with epsilon ∈ {0, 0.01, 0.05}.
- Automatic generation of: payoff matrix (CSV + heatmap), ranking, cooperation curves.

---

## 11. Useful Experiment Examples

1. **Noise robustness**: TFT vs PAVLOV vs GTFT varying epsilon.
2. **Variable horizon**: Short vs long n_rounds; different delta (continuation probability).
3. **Cartel vs deviators**: ALLC dominated by ALLD; introduction of GRIM and stability.
4. **Evolutionary**: Mixed population TFT/PAVLOV/ALLD/GTFT with low mutation.
5. **ZD**: Comparison Extortion vs Generous with moderate noise.

---

## 12. Code Quality Guidelines

- Complete type hints; mypy optional.
- Docstrings with decision formula and bibliographic references.
- Consistent naming (C/D, epsilon, delta, n_rounds).
- Clear separation between core and app (no I/O in core; core works on data objects).
- Seed managed centrally (`utils.make_rng(seed)`), propagated to all components.
- Config-driven: experiments do not require code changes.

---

## 13. Appendix: Strategy Definitions (Pseudo-code)

- **ALLC**: `return 'C'`
- **ALLD**: `return 'D'`
- **TFT**: First C; then `opp_last`
- **TF2T**: Defect if opponent defected in last two rounds
- **GRIM**: Flag `betrayed`; cooperate while `betrayed=False`; if sees D → `betrayed=True` and then D forever
- **PAVLOV (WSLS)**: Repeat your last move if last round payoff ≥ R (or equivalent rule based on joint move: stay if CC or DD, change if CD or DC)
- **RANDOM(p)**: `return 'C'` with prob. p
- **GTFT**: Like TFT but if `opp_last=='D'`, cooperate with prob. `forgive_p`
- **NoisyTFT**: Like TFT but ignores a single isolated D (memory=2/3) or uses a counter of "tolerated errors"

---

## 14. Output Data: Recommended Schema

### matches.csv (per match A vs B)

```csv
exp_id, rep, A, B, round, a_action, b_action, a_payoff, b_payoff, state, cum_a, cum_b
```

### summary.csv (average over repetitions)

```csv
exp_id, A, B, mean_payoff_A, mean_payoff_B, coop_A, coop_B, cc_rate, cd_rate, dc_rate, dd_rate
```

### ranking.csv (per strategy)

```csv
exp_id, strategy, mean_payoff, std_payoff, mean_coop_rate
```

---

## 15. Checkpoint: What to Implement Before Writing Code

- Confirm default payoff parameters (T=5, R=3, P=1, S=0).
- Decide initial strategy set and relative parameters (e.g., p for RANDOM, `forgive_p` for GTFT).
- Choose whether to include delta (continuation) already in MVP or in next step.
- Define plot format and file naming.
- Establish seeding policy (e.g., base seed and offset per run).

---

## 16. References

- R. Axelrod, *The Evolution of Cooperation*.
- Press & Dyson (2012), *Iterated Prisoner's Dilemma contains strategies that dominate any evolutionary opponent*.

---

## 17. Completed Implementations

### 17.1 Visualizations (`prisoners_dilemma/visuals/plots.py`)

- `cooperation_curve(log)`: Time series of cumulative cooperation rate for a match.
- `plot_leaderboard(leaderboard)`: Horizontal bar chart of tournament ranking.
- `plot_payoff_heatmap(results)`: Heatmap of mean payoffs for each strategy vs strategy matchup.
- `plot_cooperation_heatmap(results)`: Heatmap of cooperation rates for each matchup.
- `plot_payoff_distribution(results)`: Box plot of payoff distribution per strategy.
- `plot_match_timeseries(log, player_a_name, player_b_name)`: Time series with cooperation rate and cumulative payoff for a specific match.

### 17.2 Tournament Script with Visualizations (`prisoners_dilemma/examples/tournament_with_plots.py`)

- Runs a complete round-robin tournament with 8 strategies (ALLC, ALLD, TFT, TF2T, GRIM, PAVLOV, GTFT, RAND).
- Automatically generates all visualizations and saves them in timestamped directories (`data/results/tournament_YYYYMMDD_HHMMSS/`).
- Includes time series for interesting matchups (TFT vs GRIM, PAVLOV vs GTFT, TFT vs ALLD).
- Saves a text summary file with tournament statistics.
- Configurable parameters: `n_rounds=200`, `repetitions=5`, noise `epsilon=0.02`.

### 17.3 Added Dependencies

- `numpy>=1.24`: Used for array operations in heatmaps and visualizations.

---

## Conclusion

This guide defines responsibilities, APIs, pipelines, and quality standards for building a robust and extensible framework for PD/IPD. Following the roadmap order will ensure a working MVP and, in subsequent iterations, advanced analysis and visualizations.
