# planner.py
import random
from copy import deepcopy

NUM_MATCHES = 6
NUM_COURTS = 3
PLAYERS_PER_COURT = 4  # two teams of 2

def generate_round_from_players(players):
    """Given 12 players, generate one round (3 courts) with 2v2 each."""
    assert len(players) == 12
    p = players.copy()
    random.shuffle(p)
    courts = []
    for i in range(NUM_COURTS):
        slice_players = p[i*PLAYERS_PER_COURT:(i+1)*PLAYERS_PER_COURT]
        random.shuffle(slice_players)
        team_a = slice_players[:2]
        team_b = slice_players[2:]
        courts.append({
            "court_id": i+1,
            "team_a": team_a,
            "team_b": team_b
        })
    return courts

def generate_full_schedule(players):
    """Generate NUM_MATCHES rounds. Attempt to minimize repeated teammates by simple heuristic."""
    if len(players) != 12:
        raise ValueError("Need exactly 12 players")
    all_matches = []
    # Simple approach: for each match generate a round, try to reduce repeated teammates by retrying few times.
    teammates = {p:set() for p in players}
    for match_id in range(1, NUM_MATCHES+1):
        best = None
        best_score = None
        # try many shuffles and choose the one maximizing new teammate pairs
        for _ in range(200):  # try 200 shuffles
            courts = generate_round_from_players(players)
            score = 0
            for c in courts:
                for pair in (c["team_a"], c["team_b"]):
                    a,b = pair
                    if b not in teammates[a]:
                        score += 1
            if best is None or score > best_score:
                best = courts
                best_score = score
                if score == NUM_COURTS*2:  # maximal possible for a round
                    break
        # update teammates
        for c in best:
            for a,b in (c["team_a"], c["team_b"]):
                teammates[a].add(b)
                teammates[b].add(a)
        all_matches.append({
            "match_id": match_id,
            "courts": deepcopy(best)
        })
    return all_matches
