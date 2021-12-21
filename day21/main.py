from collections import defaultdict
from dataclasses import dataclass
import os.path
from typing import Iterator, Literal

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))

DIRAC_ROLLS = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1,
}


@dataclass(frozen=True)
class GameState:
    p1_position: int
    p2_position: int
    p1_score: int
    p2_score: int
    active_player: Literal[1, 2]

    def move_active_player(self, amount: int) -> "GameState":
        active_player = self.active_player
        if active_player == 1:
            new_position = mod(self.p1_position + amount, 10)
            return GameState(
                p1_position=new_position,
                p2_position=self.p2_position,
                p1_score=self.p1_score + new_position,
                p2_score=self.p2_score,
                active_player=2,
            )
        elif self.active_player == 2:
            new_position = mod(self.p2_position + amount, 10)
            return GameState(
                p1_position=self.p1_position,
                p2_position=new_position,
                p1_score=self.p1_score,
                p2_score=self.p2_score + new_position,
                active_player=1,
            )
        raise RuntimeError


def parse_start(raw_start: str) -> int:
    return int(raw_start.strip()[-1])


def deterministic_die() -> Iterator[int]:
    while True:
        for i in range(1, 101):
            yield i


def mod(a: int, n: int) -> int:
    return ((a - 1) % n) + 1


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        raw_p1_start, raw_p2_start = f.readlines()
    p1_start = parse_start(raw_p1_start)
    p2_start = parse_start(raw_p2_start)

    player_states = {
        1: (p1_start, 0),
        2: (p2_start, 0),
    }
    die = deterministic_die()
    d_count = 0

    while max(score for _, score in player_states.values()) < 1000:
        for player, (position, score) in player_states.items():
            move = next(die) + next(die) + next(die)
            d_count += 3
            position = mod(position + move, 10)
            score += position
            player_states[player] = (position, score)
            if score >= 1000:
                break

    answer_1 = min(score for _, score in player_states.values()) * d_count
    assert answer_1 == 576600
    print(answer_1)

    game_states: defaultdict[GameState, int] = defaultdict(int)
    game_states[GameState(
        p1_position=p1_start,
        p2_position=p2_start,
        p1_score=0,
        p2_score=0,
        active_player=1,
    )] += 1
    p1_wins = 0
    p2_wins = 0
    while game_states:
        new_game_states: defaultdict[GameState, int] = defaultdict(int)
        for game_state, state_multiplicity in game_states.items():
            for roll, roll_multiplicity in DIRAC_ROLLS.items():
                new_state = game_state.move_active_player(roll)
                new_multiplicity = state_multiplicity * roll_multiplicity
                if new_state.p1_score >= 21:
                    p1_wins += new_multiplicity
                elif new_state.p2_score >= 21:
                    p2_wins += new_multiplicity
                else:
                    new_game_states[new_state] += new_multiplicity
        game_states = new_game_states

    answer_2 = max(p1_wins, p2_wins)
    assert answer_2 == 131888061854776
    print(answer_2)


if __name__ == "__main__":
    main()
