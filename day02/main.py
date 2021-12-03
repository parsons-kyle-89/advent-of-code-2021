from dataclasses import dataclass
from enum import Enum
import os.path

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


class Direction(Enum):
    UP = 'up'
    DOWN = 'down'
    FORWARD = 'forward'


@dataclass(frozen=True)
class Move:
    direction: Direction
    distance: int


def parse_move(raw_move: str) -> Move:
    direction, distance = raw_move.split(maxsplit=1)

    direction = Direction(direction)
    distance = int(distance)

    return Move(direction, distance)


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        moves = [parse_move(raw_move) for raw_move in f.readlines()]

    horiz, depth = 0, 0
    for move in moves:
        match move:
            case Move(Direction.FORWARD, distance):
                horiz += distance
            case Move(Direction.UP, distance):
                depth -= distance
            case Move(Direction.DOWN, distance):
                depth += distance

    answer_1 = horiz * depth
    assert answer_1 == 1690020
    print(answer_1)

    horiz, depth, aim = 0, 0, 0
    for move in moves:
        match move:
            case Move(Direction.FORWARD, distance):
                horiz += distance
                depth += distance * aim
            case Move(Direction.UP, distance):
                aim -= distance
            case Move(Direction.DOWN, distance):
                aim += distance

    answer_2 = horiz * depth
    assert answer_2 == 1408487760
    print(answer_2)


if __name__ == "__main__":
    main()
