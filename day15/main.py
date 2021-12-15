from itertools import product
from operator import itemgetter
import os.path

import numpy as np
from scipy.sparse import csr_matrix

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


def total_risk(risk, start: tuple[int, int], end: tuple[int, int], seen: set[tuple[int, int]]):
    max_x, max_y = risk.shape
    end_x, end_y = end
    if start == end:
        return 0
    neighbors = [
        (x, y) 
        for x, y in ((end_x - 1, end_y), (end_x, end_y - 1))
        if (x, y) not in seen
        if 0 <= x < max_x
        if 0 <= y < max_y
    ]
    return risk[end_x, end_y] + min(total_risk(risk, start, neighbor, {end, *seen}) for neighbor in neighbors)


def risk_to_adj(risk):
    width, height = risk.shape
    adj = np.full((width * height, width * height), np.inf, float)
    for x, y in product(range(width), range(height)):
        index = get_index(x, y)
        for neighbor_x, neighbor_y in neighbors(x, y, width, height):
            neighbor_index = get_index(neighbor_x, neighbor_y)
            adj[index, neighbor_index] = risk[neighbor_x, neighbor_y]
    return adj


def get_index(x: int, y: int) -> int:
    return x + 10 * y


def neighbors(x: int, y: int, max_x: int, max_y: int) -> list[tuple[int, int]]:
    return [
        (xx, yy) 
        for xx, yy in ((x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1))
        if 0 <= xx < max_x
        if 0 <= yy < max_y
    ]


def tropical_product(a, b):
    return np.min(a[:,:,None]+b[None,:,:], axis=1)


def dijkstra(risk, start: tuple[int, int], end: tuple[int, int]) -> int:
    width, height = risk.shape
    nodes = list(product(range(width), range(height)))
    unvisited = set(nodes)
    tentative_distances = {node: float('inf') for node in nodes}
    tentative_distances[start] = 0
    possible_current = {start}

    while end in unvisited:
        current = min(possible_current, key=lambda node: tentative_distances[node])
        possible_current.remove(current)
        current_x, current_y = current
        for neighbor in neighbors(current_x, current_y, width, height):
            if neighbor in unvisited:
                neighbor_x, neighbor_y = neighbor
                possible_current.add(neighbor)
                tentative_distances[neighbor] = min(tentative_distances[neighbor], tentative_distances[current] + risk[neighbor_x, neighbor_y])
        unvisited.remove(current)
    return tentative_distances[end]


def rotate_risk(risk, amount: int):
    return (((risk + amount - 1) % 9) + 1)



def main() -> None:
    np.set_printoptions(threshold=np.inf)
    np.set_printoptions(linewidth=100000)

    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        raw_rows = f.readlines()

    width = len(raw_rows[0]) - 1
    height = len(raw_rows)
    risk = np.zeros((height, width), int)
    for y, row in enumerate(raw_rows):
        for x, cell in enumerate(row.strip()):
            risk[y, x] = int(cell)
    answer_1 = dijkstra(risk, (0, 0), (99, 99))

    assert answer_1 == 604
    print(answer_1)

    bigger_risk = np.zeros((height * 5, width * 5), int)
    for i, j in product(range(5), range(5)):
        bigger_risk[i*width:(i+1)*width, j*height:(j+1)*height] = rotate_risk(risk, i + j)
    answer_2 = dijkstra(bigger_risk, (0, 0), (499, 499))

    assert answer_2 == 2907
    print(answer_2)


if __name__ == "__main__":
    main()
