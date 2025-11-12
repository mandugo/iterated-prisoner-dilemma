 Guida completa per progettare e simulare il (Iterated) Prisoner’s Dilemma in Python

Obiettivo: progettare un framework Python modulare e testabile per simulare Prisoner’s Dilemma (PD) e Iterated Prisoner’s Dilemma (IPD), eseguire tornei tra strategie, analizzare i risultati e visualizzare i comportamenti.

⸻

1) Requisiti e scopo

Requisiti funzionali
	•	Simulare una singola partita (one-shot PD) e partite ripetute (IPD) con numero di round fisso o casuale (geometricamente terminante).
	•	Gestire rumore/errori d’azione (es. flip di una mossa con probabilità epsilon).
	•	Definire un set di strategie estendibile via interfaccia/astrazione comune.
	•	Eseguire match 1-vs-1, tornei all-play-all, round-robin e popolazioni evolutive (replicator dynamics).
	•	Calcolare e salvare metriche (payoff medio, tasso di cooperazione, lunghezze di run, transizioni di stato, punteggi per round…).
	•	Fornire visualizzazioni (curve temporali, distribuzioni, matrici di payoff, heatmap di cooperazione, diagrammi di stato, dinamica evolutiva).
	•	Riproducibilità: semi random, configurazioni versionate (YAML/JSON), logging.

Requisiti non funzionali
	•	Codice pulito e tipizzato (type hints), semplice da testare (pytest), documentato (docstring + README/agents.md).
	•	Struttura a pacchetto Python con separazione netta tra core, strategie, esecuzione esperimenti e plotting.
	•	Performance: evitare bottleneck (uso di numpy dove utile), opzione di parallelizzazione (multiprocessing) per tornei grandi.

⸻

2) Struttura del progetto

prisoners_dilemma/
├─ pd_core/
│  ├─ __init__.py
│  ├─ game.py              # logica di PD/IPD, PayoffMatrix, Match, Series
│  ├─ strategy.py          # interfaccia Strategy, util comuni per memoria stato
│  ├─ player.py            # wrapper Agent/Player (strategy + stato)
│  ├─ tournament.py        # round-robin, all-play-all, campionati, bracket
│  ├─ evo.py               # dinamiche evolutive (replicator, mutazione)
│  ├─ metrics.py           # raccolta/aggregazione metriche
│  ├─ noise.py             # modelli di rumore (flip, osservazione imperfetta)
│  └─ utils.py             # RNG, seed, helper
│
├─ strategies/
│  ├─ __init__.py
│  ├─ base.py              # classi base/primitive comuni
│  ├─ simple.py            # ALLC, ALLD, TFT, TF2T, Grim, Pavlov
│  ├─ probabilistic.py     # Random(p), GenerousTFT, vellutate
│  ├─ memory.py            # memorie più lunghe, correttori di rumore
│  ├─ zd.py                # Zero-Determinant (opzionale avanzato)
│  └─ ml.py                # strategie adattive/evolutive (placeholder)
│
├─ experiments/
│  ├─ configs/             # YAML di esperimenti (parametri, seed, roster)
│  ├─ run_experiment.py    # entrypoint CLI per lanciare esperimenti
│  ├─ analyze_results.py   # script di analisi/plot
│  └─ notebooks/           # (opzionale) esplorazioni Jupyter
│
├─ visuals/
│  ├─ plots.py             # API ad alto livello per grafici
│  └─ styles.py            # regole estetiche comuni (senza imporre colori)
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
└─ agents.md               # questo file-guida


⸻

3) Modello del gioco

3.1 Scelte e payoff
	•	Azioni: C (Cooperate), D (Defect).
	•	Payoff standard: T>R>P>S (es. T=5, R=3, P=1, S=0).
	•	Matrice dei payoff (per il giocatore A; B è simmetrica):
	•	(C,C) → R
	•	(C,D) → S
	•	(D,C) → T
	•	(D,D) → P

Il sistema deve permettere payoff personalizzati e versionati.

3.2 Rumore (noise models)
	•	Action flip: con probabilità epsilon, l’azione scelta viene invertita.
	•	Observation noise (opzionale): ciascun giocatore osserva con errore l’azione avversaria.
	•	Start noise: mossa iniziale randomizzata con bias.

3.3 Orizzonte del gioco IPD
	•	Fisso: n_rounds.
	•	Stocastico: continuazione con probabilità delta (equivalente a sconto geometrico).

⸻

4) Architettura delle classi

4.1 Interfaccia Strategy

class Strategy(Protocol):
    name: str
    def reset(self) -> None: ...
    def first_move(self, rng: random.Random) -> str: ...  # 'C' o 'D'
    def next_move(self, my_last: str | None, opp_last: str | None, rng: random.Random) -> str: ...

	•	Stateless vs stateful: alcune strategie mantengono memoria (es. GRIM, PAVLOV). State da azzerare con reset().
	•	Memoria estesa: fornire mixin/util per accedere alla storia degli esiti se necessario (lista di tuple di mosse o payoff).
	•	Parametri: ogni strategia deve accettare parametri nel costruttore (es. p per Random, probabilità di perdono per GTFT).

4.2 Player/Agent

@dataclass
class Player:
    strategy: Strategy
    id: str | None = None

	•	Wrapper per tracciare identità e istanza di strategia.

4.3 PayoffMatrix

@dataclass(frozen=True)
class PayoffMatrix:
    R: int
    S: int
    T: int
    P: int
    def payoff(self, a: str, b: str) -> tuple[int, int]: ...

4.4 Match (one-shot) e Series (IPD)

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

	•	Raccogliere telemetria per round (azioni, payoff, stati) per analisi fine-grained.

4.5 Tournament API

@dataclass
class TournamentConfig:
    roster: list[Player]             # o fabbriche di strategie
    matrix: PayoffMatrix
    n_rounds: int
    delta: float | None
    noise: Noise | None
    repetitions: int = 1            # ripetere match per mediare il rumore
    pairing: Literal['round_robin','all_play_all','double_rr'] = 'round_robin'
    parallel: bool = False
    seed: int | None = None

class Tournament:
    def run(self, cfg: TournamentConfig) -> TournamentResult: ...

4.6 Evoluzione (opzionale ma raccomandata)

@dataclass
class EvolutionConfig:
    strategies: list[type[Strategy]] | list[Callable[[], Strategy]]
    population: dict[str, int]            # per strategia → numerosità
    fitness: Literal['mean_payoff','median','coop_rate'] = 'mean_payoff'
    mutation_rate: float = 0.0
    generations: int = 200
    tournament_cfg: TournamentConfig      # riusa regole IPD

class Evolution:
    def run(self, cfg: EvolutionConfig) -> EvolutionResult: ...

	•	Dinamiche replicator: proporzione ∝ fitness relativa; aggiungere mutazione/invasori rari.

⸻

5) Strategie da implementare (MVP → avanzate)

MVP (baseline solide)
	1.	ALLC (Always Cooperate)
	2.	ALLD (Always Defect)
	3.	TFT (Tit for Tat)
	4.	TF2T (Tit for Two Tats)
	5.	GRIM (Grim Trigger)
	6.	PAVLOV / Win-Stay, Lose-Shift
	7.	RANDOM(p) (mista Bernoulli)
	8.	GTFT (Generous Tit for Tat; parametro forgive_p)

Avanzate (rumore/memoria)
	9.	NoisyTFT (correttore di errori singoli, memoria 2–3)
	10.	Adaptive (stima p(C|stato) dell’avversario, myopic best response)

Extra (research)
	11.	Zero-Determinant (Press & Dyson; extortionate e generous)
	12.	Evolutive/ML (genetiche, Q-learning; placeholder con interfaccia coerente)

Ogni strategia deve definire: name, parametri, reset, first_move, next_move, docstring con riferimenti.

⸻

6) Metriche e logging

Metriche per match/serie
	•	Payoff cumulativo e medio (per giocatore e totale).
	•	Tasso di cooperazione per giocatore e congiunto (frazione di C).
	•	Transizioni di stato: conteggio di (CC, CD, DC, DD), matrice 2×2.
	•	Streaks: lunghezze di run di C/D.
	•	Stazionarietà: tempo per convergere a pattern ricorrenti.

Metriche di torneo
	•	Classifica (media e varianza del payoff per strategia).
	•	Matrice payoff (riga: strategia A; colonna: strategia B → payoff medio A vs B).
	•	Cooperazione media per match-up.
	•	Robustezza al rumore: curve al variare di epsilon/delta/n_rounds.

Persistenza dei risultati
	•	Salvare in CSV/Parquet: results/matches.csv, results/summary.csv.
	•	Salvare config (YAML) e seed usati per tracciabilità.

⸻

7) Visualizzazioni (plots) — linee guida

Le visualizzazioni saranno implementate con matplotlib, evitando stili/colore forzati a priori e grafici sovraccarichi.

	1.	Time series: payoff per round, cooperazione cumulata, stato (CC, CD, DC, DD) per una coppia di strategie.
	2.	Heatmap: payoff medio di A contro B; cooperazione media di A contro B.
	3.	Distribuzioni: istogrammi/ECDF dei payoff medi per strategia (su ripetizioni).
	4.	Curva rumore: payoff medio vs epsilon; cooperazione vs epsilon (più strategie sulla stessa figura separate).
	5.	Dinamica evolutiva: simplex/line-chart delle frequenze di popolazione nel tempo (generazioni).
	6.	Diagrammi di stato (piccoli): transizioni tra CC, CD, DC, DD con spessori proporzionali (salvare come PNG/SVG).

Ogni grafico deve avere: titolo informativo, assi etichettati, legenda chiara, annotazioni minime per insight principali.

⸻

8) Pipeline di esperimenti

8.1 Config YAML (esempio)

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

8.2 Esecuzione
	•	python experiments/run_experiment.py --config experiments/configs/exp001.yaml
	•	Opzioni CLI: override di n_rounds, epsilon, repetitions, parallel, output_dir.

8.3 Analisi
	•	python experiments/analyze_results.py --input data/results/exp001
	•	Produce tabelle riassuntive + grafici in data/results/exp001/plots/.

⸻

9) Dettagli implementativi chiave

9.1 Rumore
	•	Implementare Noise come callable:

@dataclass
class Noise:
    epsilon: float = 0.0
    def apply(self, action: str, rng: Random) -> str:
        return action if rng.random() > self.epsilon else ('D' if action=='C' else 'C')

	•	Integrare nel loop del gioco subito dopo la scelta dell’azione e prima del payoff.

9.2 Loop IPD (bozza)

A.strategy.reset(); B.strategy.reset()
a_prev = b_prev = None
for t in range(n_rounds) or while rng.random() < delta:
    a = A.strategy.first_move(rng) if t == 0 else A.strategy.next_move(a_prev, b_prev, rng)
    b = B.strategy.first_move(rng) if t == 0 else B.strategy.next_move(b_prev, a_prev, rng)
    a_eff = noise.apply(a, rng) if noise else a
    b_eff = noise.apply(b, rng) if noise else b
    pa, pb = matrix.payoff(a_eff, b_eff)
    # loggare azioni effettive e payoff; aggiornare prev
    a_prev, b_prev = a_eff, b_eff

9.3 Metriche efficienti
	•	Calcolare on-the-fly: contatori nC_A, nC_B, cc, cd, dc, dd, somme payoff.
	•	Al termine, derivare ratei e medie.

9.4 Parallelizzazione tornei
	•	Usare multiprocessing.Pool o concurrent.futures.ProcessPoolExecutor per parallelizzare i match.
	•	Passare seed derivati (es. seed_base + hash(pairing)) per indipendenza.

9.5 Test (pytest)
	•	PayoffMatrix: coerenza T>R>P>S; mapping corretto.
	•	Noise: frequenza di flip ≈ epsilon su grande N.
	•	Strategie: casi base (ALLC vs ALLD), TFT reciproco, GRIM punisce.
	•	Game: conservazione lunghezza, tassi cooperazione attesi.
	•	Tournament: determinismo per epsilon=0, repetitions=1, seed fisso.

⸻

10) Strategia di sviluppo (roadmap)
	1.	Core minimo: PayoffMatrix, Strategy (protocol), Noise, Game/IteratedGame con logging minimi.
	2.	Strategie MVP: ALLC, ALLD, TFT, GRIM, PAVLOV, TF2T, RANDOM(p), GTFT.
	3.	Metriche: oggetti risultato e funzioni di aggregazione; salvataggio CSV.
	4.	Tournament: round-robin con ripetizioni; CLI semplice.
	5.	Visuals: time series, heatmap payoff, ranking bar chart.
	6.	Rumore avanzato: NoisyTFT, osservazione imperfetta.
	7.	Evoluzione: replicator + mutazione; grafici dinamica.
	8.	Ottimizzazioni: parallel, numpy, caching.
	9.	QA: test + docs; esempi riproducibili.

Criteri di “Done” per MVP:
	•	Torneo tra 6–8 strategie su 200 round × 20 ripetizioni con epsilon ∈ {0, 0.01, 0.05}.
	•	Generazione automatica di: matrice payoff (CSV + heatmap), classifica, curve cooperazione.

⸻

11) Esempi di esperimenti utili
	1.	Robustezza al rumore: TFT vs PAVLOV vs GTFT al variare di epsilon.
	2.	Orizzonte variabile: n_rounds corto vs lungo; delta (continuation probability) diversa.
	3.	Cartello vs deviatori: ALLC dominata da ALLD; introduzione di GRIM e stabilità.
	4.	Evolutivo: popolazione mista TFT/PAVLOV/ALLD/GTFT con bassa mutazione.
	5.	ZD: confronto Extortion vs Generous con rumore moderato.

⸻

12) Linee guida di qualità del codice
	•	Type hints completi; mypy opzionale.
	•	Docstring con formula della decisione e riferimenti bibliografici.
	•	Naming consistente (C/D, epsilon, delta, n_rounds).
	•	Separazione netto tra core e app (no I/O nel core; il core lavora su oggetti dati).
	•	Seed gestito centralmente (utils.make_rng(seed)), propagato a tutti i componenti.
	•	Config-driven: gli esperimenti non richiedono modifiche al codice.

⸻

13) Appendice: definizioni delle strategie (pseudo)
	•	ALLC: return 'C'.
	•	ALLD: return 'D'.
	•	TFT: prima C; poi opp_last.
	•	TF2T: difetta se opp ha defezionato negli ultimi due round.
	•	GRIM: flag betrayed; coopera finché betrayed=False; se vede D → betrayed=True e allora D per sempre.
	•	PAVLOV (WSLS): ripeti la tua ultima mossa se payoff dell’ultimo round ≥ R (o regola equivalente basata su mossa congiunta: resta se CC o DD, cambia se CD o DC).
	•	RANDOM(p): return 'C' con prob. p.
	•	GTFT: come TFT ma se opp_last=='D', coopera con prob. forgive_p.
	•	NoisyTFT: come TFT ma ignora una singola D isolata (memoria=2/3) o usa un contatore di “errori tollerati”.

⸻

14) Output dati: schema consigliato

matches.csv (per match A vs B)

exp_id, rep, A, B, round, a_action, b_action, a_payoff, b_payoff, state, cum_a, cum_b

summary.csv (per media su ripetizioni)

exp_id, A, B, mean_payoff_A, mean_payoff_B, coop_A, coop_B, cc_rate, cd_rate, dc_rate, dd_rate

ranking.csv (per strategia)

exp_id, strategy, mean_payoff, std_payoff, mean_coop_rate


⸻

15) Checkpoint: cosa implementare prima di scrivere codice
	•	Confermare parametri di payoff default (T=5, R=3, P=1, S=0).
	•	Decidere set iniziale di strategie e relativi parametri (es. p per RANDOM, forgive_p per GTFT).
	•	Scegliere se includere delta (continuation) già nell’MVP o in step successivo.
	•	Definire formato dei plots e naming file.
	•	Stabilire politica di seeding (es. base seed e offset per run).

⸻

16) Riferimenti sintetici
	•	R. Axelrod, The Evolution of Cooperation.
	•	Press & Dyson (2012), Iterated Prisoner's Dilemma contains strategies that dominate any evolutionary opponent.

⸻

17) Implementazioni completate

17.1 Visualizzazioni (prisoners_dilemma/visuals/plots.py)
	•	cooperation_curve(log): curva temporale del tasso di cooperazione cumulativo per un match.
	•	plot_leaderboard(leaderboard): grafico a barre orizzontali della classifica del torneo.
	•	plot_payoff_heatmap(results): heatmap dei payoff medi per ogni matchup strategia vs strategia.
	•	plot_cooperation_heatmap(results): heatmap dei tassi di cooperazione per ogni matchup.
	•	plot_payoff_distribution(results): box plot della distribuzione dei payoff per strategia.
	•	plot_match_timeseries(log, player_a_name, player_b_name): serie temporale con tasso di cooperazione e payoff cumulativo per un match specifico.

17.2 Script torneo con visualizzazioni (prisoners_dilemma/examples/tournament_with_plots.py)
	•	Esegue un torneo round-robin completo con 8 strategie (ALLC, ALLD, TFT, TF2T, GRIM, PAVLOV, GTFT, RAND).
	•	Genera automaticamente tutte le visualizzazioni e le salva in directory timestampate (data/results/tournament_YYYYMMDD_HHMMSS/).
	•	Include serie temporali per matchup interessanti (TFT vs GRIM, PAVLOV vs GTFT, TFT vs ALLD).
	•	Salva un file di riepilogo testuale con statistiche del torneo.
	•	Parametri configurabili: n_rounds=200, repetitions=5, noise epsilon=0.02.

17.3 Dipendenze aggiunte
	•	numpy>=1.24: utilizzato per operazioni su array nelle heatmap e visualizzazioni.

⸻

Conclusione

Questa guida definisce responsabilità, API, pipeline e standard qualitativi per costruire un framework robusto e estendibile per PD/IPD. Seguire l’ordine della roadmap garantirà un MVP funzionante e, in iterazioni successive, analisi e visualizzazioni avanzate.
