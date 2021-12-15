from collections import defaultdict
from itertools import product
import os.path
from typing import cast

import numpy as np
import numpy.typing as np_typing


SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))

Grid = np_typing.NDArray[np.int64]
Point = tuple[int, int]


def parse_risk(raw_risk: str) -> Grid:
    return np.array([parse_row(raw_row) for raw_row in raw_risk.splitlines()])


def parse_row(raw_row: str) -> list[int]:
    return [int(raw_cell) for raw_cell in raw_row.strip()]


def neighbors(point: Point, max_x: int, max_y: int) -> set[Point]:
    point_x, point_y = point
    return {
        (x, y)
        for x, y in (
            (point_x - 1, point_y), (point_x, point_y - 1),
            (point_x + 1, point_y), (point_x, point_y + 1),
        )
        if 0 <= x < max_x
        if 0 <= y < max_y
    }


def dijkstra(risk: Grid, start: Point, end: Point) -> int:
    width, height = risk.shape
    tentative_distances: defaultdict[Point, int | float] = (
        defaultdict(lambda: float('inf'))
    )
    tentative_distances[start] = 0
    visited = set()
    possible_current = {start}

    while end not in visited:
        current = min(possible_current, key=tentative_distances.__getitem__)
        possible_current.remove(current)
        visited.add(current)
        for neighbor in neighbors(current, width, height) - visited:
            neighbor_x, neighbor_y = neighbor
            possible_current.add(neighbor)
            tentative_distances[neighbor] = min(
                tentative_distances[neighbor],
                tentative_distances[current] + risk[neighbor_x, neighbor_y]
            )
    return cast(int, tentative_distances[end])


def rotate_risk(risk: Grid, amount: int) -> Grid:
    return (((risk + amount - 1) % 9) + 1)


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        raw_risk = f.read()
    risk = parse_risk(raw_risk)
    width, height = risk.shape

    answer_1 = dijkstra(risk, (0, 0), (width-1, height-1))
    assert answer_1 == 604
    print(answer_1)

    bigger_risk = np.zeros((height * 5, width * 5), int)
    for i, j in product(range(5), range(5)):
        bigger_risk[i*width:(i+1)*width, j*height:(j+1)*height] = (
            rotate_risk(risk, i + j)
        )

    answer_2 = dijkstra(bigger_risk, (0, 0), (width*5 - 1, height*5 - 1))
    assert answer_2 == 2907
    print(answer_2)


if __name__ == "__main__":
    main()
