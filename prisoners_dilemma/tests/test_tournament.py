from prisoners_dilemma.pd_core.player import Player
from prisoners_dilemma.pd_core.tournament import RoundRobinTournament
from prisoners_dilemma.strategies import AllCooperate, AllDefect


def test_round_robin_runs_all_pairs() -> None:
    players = [Player(AllCooperate()), Player(AllDefect()), Player(AllCooperate())]
    tournament = RoundRobinTournament(players, n_rounds=5, repetitions=2, seed=1)
    results = tournament.run()
    assert len(results.matches) == 3 * 2  # 3 pairs, 2 repetitions
    leaderboard = results.leaderboard()
    assert set(leaderboard) == {p.display_name for p in players}
