from typing import cast, Sequence
import os.path

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


Row = tuple[int, int, int, int, int]
Board = tuple[Row, Row, Row, Row, Row]


class Game:

    def __init__(self, board: Board):
        self._board = board
        self._flat_board = [entry for row in board for entry in row]
        self._marked = [False for _ in range(len(self._flat_board))]

    def __str__(self) -> str:
        to_print = [
            'X' if marked else str(entry)
            for entry, marked in zip(self._flat_board, self._marked)
        ]
        return '\n'.join(
            '{:>2} {:>2} {:>2} {:>2} {:>2}'.format(*to_print[5*i:5*i+5])
            for i in range(5)
        )

    def mark(self, number: int) -> None:
        try:
            idx = self._flat_board.index(number)
        except ValueError:
            pass
        else:
            self._marked[idx] = True

    def won(self) -> bool:
        return (
            any(all(self._marked[5*i:5*i+5]) for i in range(5))
            or any(all(self._marked[i::5]) for i in range(5))
        )

    def sum_unmarked(self) -> int:
        return sum(
            entry for entry, marked in zip(self._flat_board, self._marked)
            if not marked
        )

    @classmethod
    def parse(cls, raw_board: str) -> 'Game':
        raw_rows = [r.strip() for r in raw_board.split('\n', maxsplit=4)]
        board = tuple(
            tuple(int(raw_entry) for raw_entry in raw_row.split(maxsplit=4))
            for raw_row in raw_rows
        )
        return cls(cast(Board, board))


def parse_numbers(raw_numbers: str) -> list[int]:
    return [int(raw_number) for raw_number in raw_numbers.split(',')]


def simulate_winning(
    games: Sequence[Game],
    numbers: Sequence[int]
) -> tuple[Game, int]:
    winners = []
    for number in numbers:
        for game in games:
            game.mark(number)
            if game.won():
                winners.append(game)
        if winners:
            break
    assert len(winners) == 1
    winner = winners[0]
    return winner, number


def simulate_losing(
    games: Sequence[Game],
    numbers: Sequence[int]
) -> tuple[Game, int]:
    for number in numbers:
        newly_won: list[Game] = []
        for game in games:
            game.mark(number)
            if game.won():
                newly_won.append(game)
        games = [game for game in games if game not in newly_won]
        if not games:
            break
    assert len(newly_won) == 1
    loser = newly_won[0]
    return loser, number


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        raw_numbers = f.readline()
        raw_boards = f.read().strip().split('\n\n')

    numbers = parse_numbers(raw_numbers)
    games = [Game.parse(raw_board) for raw_board in raw_boards]

    winner, winning_number = simulate_winning(games, numbers)
    answer_1 = winner.sum_unmarked() * winning_number

    assert answer_1 == 49686
    print(answer_1)

    loser, losing_number = simulate_losing(games, numbers)
    answer_2 = loser.sum_unmarked() * losing_number

    assert answer_2 == 26878
    print(answer_2)


if __name__ == "__main__":
    main()
