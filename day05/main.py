from collections import defaultdict
import os.path
from typing import Iterator, MutableMapping

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


Point = tuple[int, int]
Line = tuple[Point, Point]
Atlas = MutableMapping[Point, int]


def my_range(start: int, end: int) -> Iterator[int]:
    sign = 1 if end > start else -1
    yield from range(start, end + sign, sign)


def parse_line(raw_line: str) -> Line:
    raw_start, raw_end = raw_line.split(' -> ', maxsplit=1)
    start = parse_point(raw_start)
    end = parse_point(raw_end)
    return (start, end)


def parse_point(raw_point: str) -> Point:
    x, y = raw_point.split(',', maxsplit=1)
    return (int(x), int(y))


def line_is_ver(line: Line) -> bool:
    start, end = line
    start_x, _ = start
    end_x, _ = end
    return start_x == end_x


def line_is_hor(line: Line) -> bool:
    start, end = line
    _, start_y = start
    _, end_y = end
    return start_y == end_y


def line_is_diag(line: Line) -> bool:
    start, end = line
    start_x, start_y = start
    end_x, end_y = end
    return abs(end_x - start_x) == abs(end_y - start_y)


def ver_line_range(ver_line: Line) -> Iterator[Point]:
    start, end = ver_line
    start_x, start_y = start
    end_x, end_y = end
    assert start_x == end_x
    for y in my_range(start_y, end_y):
        yield (start_x, y)


def hor_line_range(hor_line: Line) -> Iterator[Point]:
    start, end = hor_line
    start_x, start_y = start
    end_x, end_y = end
    assert start_y == end_y
    for x in my_range(start_x, end_x):
        yield (x, start_y)


def diag_line_range(diag_line: Line) -> Iterator[Point]:
    start, end = diag_line
    start_x, start_y = start
    end_x, end_y = end
    assert abs(end_x - start_x) == abs(end_y - start_y)
    yield from zip(my_range(start_x, end_x), my_range(start_y, end_y))


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        lines = [parse_line(raw_line) for raw_line in f.readlines()]

    atlas: Atlas = defaultdict(int)
    for line in lines:
        if line_is_hor(line):
            for p in hor_line_range(line):
                atlas[p] += 1
        elif line_is_ver(line):
            for p in ver_line_range(line):
                atlas[p] += 1

    answer_1 = sum(1 for value in atlas.values() if value > 1)
    assert answer_1 == 5835
    print(answer_1)

    for line in lines:
        if line_is_diag(line):
            for p in diag_line_range(line):
                atlas[p] += 1

    answer_2 = sum(1 for value in atlas.values() if value > 1)
    assert answer_2 == 17013
    print(answer_2)


if __name__ == "__main__":
    main()
