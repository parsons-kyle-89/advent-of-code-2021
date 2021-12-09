from typing import Iterator
import os.path

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))
MAX_HEIGHT = 9
Point = tuple[int, int]


def parse_heights(raw_rows: list[str]) -> list[list[int]]:
    return [[int(h) for h in raw_row.strip()] for raw_row in raw_rows]


def neighbor_indices(x: int, y: int) -> tuple[Point, ...]:
    return (
        (x - 1, y),
        (x, y - 1),
        (x + 1, y),
        (x, y + 1),
    )


class HeightMap:

    def __init__(self, heights: list[list[int]]):
        self._heights = heights

    def __getitem__(self, point: Point) -> int:
        x, y = point
        if x < 0 or y < 0:
            return MAX_HEIGHT
        try:
            return self._heights[y][x]
        except IndexError:
            return MAX_HEIGHT

    def __iter__(self) -> Iterator[int]:
        yield from (h for row in self._heights for h in row)

    def indices(self) -> Iterator[Point]:
        yield from (
            (x, y)
            for y in range(len(self._heights))
            for x in range(len(self._heights[y]))
        )

    def neighbors(
        self, x: int,
        y: int,
        excluding: set[Point] = set(),
    ) -> tuple[int, ...]:
        _neighbors = set(neighbor_indices(x, y)) - excluding
        return tuple(self[xx, yy] for xx, yy in _neighbors)

    def is_min(self, x: int, y: int) -> bool:
        return self[x, y] < min(self.neighbors(x, y))


def basin(height_map: HeightMap, x: int, y: int) -> set[Point]:
    partial_basin = {(x, y)}
    border = {(x, y)}
    while border:
        border = {
            (xx, yy)
            for x, y in border
            for xx, yy in neighbor_indices(x, y)
            if height_map[xx, yy] <= min(
                height_map.neighbors(xx, yy, excluding=partial_basin),
                default=MAX_HEIGHT
            )
            if height_map[xx, yy] < 9
            if (xx, yy) not in partial_basin
        }
        partial_basin.update(border)
    return partial_basin


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        raw_rows = f.readlines()
    heights = parse_heights(raw_rows)

    height_map = HeightMap(heights)
    mins = {
        (x, y): h
        for h, (x, y) in zip(height_map, height_map.indices())
        if height_map.is_min(x, y)
    }

    answer_1 = sum(mins.values()) + len(mins)
    assert answer_1 == 607
    print(answer_1)

    *_, a, b, c = sorted(len(basin(height_map, x, y)) for x, y in mins.keys())
    answer_2 = a * b * c
    assert answer_2 == 900864
    print(answer_2)


if __name__ == "__main__":
    main()
