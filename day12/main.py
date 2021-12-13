from collections import defaultdict
import os.path
from typing import Sequence

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))

Graph = dict[str, set[str]]


def parse_edge(edge: str) -> tuple[str, str]:
    v1, v2 = edge.strip().split('-', maxsplit=1)
    return v1, v2


def parse_graph(raw_edges: list[str]) -> Graph:
    graph = defaultdict(set)
    for raw_edge in raw_edges:
        v1, v2 = parse_edge(raw_edge)
        graph[v1].add(v2)
        graph[v2].add(v1)
    return dict(graph)


def paths(
    graph: Graph,
    end: str,
    initial_path: list[str],
    *,
    small_cave_bonus: int = 0,
    small_cave_bonus_exclusions: Sequence[str] = ('start', 'end'),
) -> list[list[str]]:
    small_cave_path = [v for v in initial_path if v == v.lower()]
    small_cave_repeats = len(small_cave_path) - len(set(small_cave_path))
    small_cave_bonus_available = small_cave_bonus > small_cave_repeats
    current_vertex = initial_path[-1]
    if current_vertex == end:
        return [initial_path]
    return [
        full_path
        for neighbor in graph[current_vertex]
        if (
            neighbor not in initial_path
            or neighbor == neighbor.upper()
            or (
                small_cave_bonus_available
                and neighbor not in small_cave_bonus_exclusions
            )
        )
        for full_path in paths(
            graph, end, initial_path + [neighbor],
            small_cave_bonus=small_cave_bonus,
            small_cave_bonus_exclusions=small_cave_bonus_exclusions
        )
    ]


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        raw_edges = f.readlines()
    graph = parse_graph(raw_edges)
    answer_1 = len(paths(graph, 'end', ['start']))

    assert answer_1 == 4411
    print(answer_1)

    answer_2 = len(paths(graph, 'end', ['start'], small_cave_bonus=1))
    assert answer_2 == 136767
    print(answer_2)


if __name__ == "__main__":
    main()
