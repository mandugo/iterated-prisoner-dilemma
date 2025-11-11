# Iterated Prisoner's Dilemma Framework

Questo pacchetto Python fornisce un'implementazione modulare del
Prisoner's Dilemma ripetuto (IPD). Include classi per simulare match,
strategie classiche, tornei round-robin e strumenti basilari per
l'analisi dei risultati.

## Requisiti

* Python 3.11+
* `pytest` per eseguire i test automatici.

## Utilizzo rapido

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

## Test

```bash
pytest prisoners_dilemma/tests
```
