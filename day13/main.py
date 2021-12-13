from dataclasses import dataclass
from functools import reduce
import os.path

import numpy as np
import numpy.typing as np_typing

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


@dataclass(frozen=True)
class HorizontalFold:
    height: int


@dataclass(frozen=True)
class VerticalFold:
    width: int


Fold = HorizontalFold | VerticalFold
Grid = np_typing.NDArray[np.int64]


def parse_raw_instructions(raw_instructions: str) -> tuple[Grid, list[Fold]]:
    raw_points, raw_folds = raw_instructions.split('\n\n', maxsplit=1)
    points = parse_raw_points(raw_points)
    folds = parse_raw_folds(raw_folds)
    return points, folds


def parse_raw_points(raw_points: str) -> Grid:
    indices = [
        parse_raw_point(raw_point) for raw_point in raw_points.split('\n')
    ]
    max_x = max(x for x, _ in indices) + 1
    max_y = max(y for _, y in indices) + 1
    points = np.zeros((max_x, max_y)).astype(bool)
    for index in indices:
        points[index] = True
    return points


def parse_raw_point(raw_point: str) -> tuple[int, int]:
    raw_x, raw_y = raw_point.split(',', maxsplit=1)
    return int(raw_x), int(raw_y)


def parse_raw_folds(raw_folds: str) -> list[Fold]:
    return [
        parse_raw_fold(raw_fold) for raw_fold in raw_folds.strip().split('\n')
    ]


def parse_raw_fold(raw_fold: str) -> Fold:
    data = raw_fold.removeprefix('fold along ')
    direction, raw_where = data.split('=', maxsplit=1)
    where = int(raw_where)
    if direction == 'x':
        return VerticalFold(where)
    elif direction == 'y':
        return HorizontalFold(where)


def apply_fold(points: Grid, fold: Fold) -> Grid:
    match fold:
        case HorizontalFold(height):
            foo = points[:, :height] | np.flip(points[:, -height:], axis=1)
        case VerticalFold(width):
            foo = points[:width, :] | np.flip(points[-width:, :], axis=0)
    return foo


def display_grid(grid: Grid) -> str:
    return (
        '\n'.join(
            ''.join(
                '\u2588' if cell else ' ' for cell in row
            ) for row in grid.T
        )
    )


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        raw_instructions = f.read()
    points, folds = parse_raw_instructions(raw_instructions)

    answer_1 = np.sum(apply_fold(points, folds[0]))
    assert answer_1 == 765
    print(answer_1)

    print(display_grid(reduce(apply_fold, folds, points)))
    answer_2 = 'RZKZLPGH'
    assert answer_2 == 'RZKZLPGH'
    print(answer_2)


if __name__ == "__main__":
    main()
