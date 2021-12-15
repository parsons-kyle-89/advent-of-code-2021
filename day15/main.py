from itertools import product
import os.path

import numpy as np
import numpy.typing as np_typing

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


def parse_risk(raw_risk: str) -> np_typing.NDArray[np.int64]:
    return np.array([parse_row(raw_row) for raw_row in raw_risk.splitlines()])


def parse_row(raw_row: str) -> list[int]:
    return [int(raw_cell) for raw_cell in raw_row.strip()]


def neighbors(
    point: tuple[int, int],
    max_x: int,
    max_y: int,
) -> list[tuple[int, int]]:
    point_x, point_y = point
    return [
        (x, y)
        for x, y in (
            (point_x - 1, point_y), (point_x, point_y - 1),
            (point_x + 1, point_y), (point_x, point_y + 1),
        )
        if 0 <= x < max_x
        if 0 <= y < max_y
    ]


def dijkstra(
    risk: np_typing.NDArray[np.int64],
    start: tuple[int, int],
    end: tuple[int, int],
) -> int:
    width, height = risk.shape
    nodes = list(product(range(width), range(height)))
    unvisited = set(nodes)
    tentative_distances = {node: float('inf') for node in nodes}
    tentative_distances[start] = 0
    possible_current = {start}

    while end in unvisited:
        current = min(possible_current, key=tentative_distances.__getitem__)
        possible_current.remove(current)
        for neighbor in neighbors(current, width, height):
            if neighbor in unvisited:
                neighbor_x, neighbor_y = neighbor
                possible_current.add(neighbor)
                tentative_distances[neighbor] = min(
                    tentative_distances[neighbor],
                    tentative_distances[current] + risk[neighbor_x, neighbor_y]
                )
        unvisited.remove(current)
    return int(tentative_distances[end])


def rotate_risk(
    risk: np_typing.NDArray[np.int64],
    amount: int,
) -> np_typing.NDArray[np.int64]:
    return (((risk + amount - 1) % 9) + 1)


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        raw_risk = f.read()
    risk = parse_risk(raw_risk)

    answer_1 = dijkstra(risk, (0, 0), (99, 99))
    assert answer_1 == 604
    print(answer_1)

    width, height = risk.shape
    bigger_risk = np.zeros((height * 5, width * 5), int)
    for i, j in product(range(5), range(5)):
        bigger_risk[i*width:(i+1)*width, j*height:(j+1)*height] = (
            rotate_risk(risk, i + j)
        )

    answer_2 = dijkstra(bigger_risk, (0, 0), (499, 499))
    assert answer_2 == 2907
    print(answer_2)


if __name__ == "__main__":
    main()
