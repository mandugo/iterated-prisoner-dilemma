# Iterated Prisoner's Dilemma Framework

Questo pacchetto Python fornisce un'implementazione modulare del
Prisoner's Dilemma ripetuto (IPD). Include classi per simulare match,
strategie classiche, tornei round-robin e strumenti basilari per
l'analisi dei risultati.

## Requisiti

* Python 3.10+
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

## Script di esempio

Gli script nella cartella `prisoners_dilemma/examples/` mostrano come utilizzare il framework:

* `basic_match.py`: esegue un match rumoroso tra Tit For Tat e Always Defect con riepilogo dei round.
* `simple_tournament.py`: avvia un torneo round-robin tra più strategie e stampa la classifica finale.

Esegui gli script direttamente oppure tramite modulo Python, ad esempio::

    python -m prisoners_dilemma.examples.basic_match


## Test

```bash
pytest prisoners_dilemma/tests
```
