import os.path

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


Point = tuple[int, int]
Line = tuple[Point, Point]
Atlas = dict[Point, int]


def parse_line(raw_line: str) -> Line:
    raw_start, raw_end = raw_line.split(' -> ', maxsplit=1)
    start = parse_point(raw_start)
    end = parse_point(raw_end)
    return (start, end)


def parse_point(raw_point: str) -> Point:
    x, y = raw_point.split(',', maxsplit=1)
    return (int(x), int(y))


def make_atlas(top_left: Point, bottom_right: Point) -> Atlas:
    start_x, start_y = top_left
    end_x, end_y = bottom_right
    return {
        (x, y): 0
        for x in range(start_x, end_x + 1)
        for y in range(start_y, end_y + 1)
    }


def add_ver_hor_line_to_atlas(atlas: Atlas, line: Line) -> None:
    start, end = line
    start_x, start_y = start
    end_x, end_y = end
    min_x, max_x = min(start_x, end_x), max(start_x, end_x)
    min_y, max_y = min(start_y, end_y), max(start_y, end_y)

    if min_x == max_x:
        for y in range(min_y, max_y + 1):
            atlas[(min_x, y)] += 1
    elif min_y == max_y:
        for x in range(min_x, max_x + 1):
            atlas[(x, min_y)] += 1
    else:
        pass


def add_ver_hor_diag_line_to_atlas(atlas: Atlas, line: Line) -> None:
    start, end = line
    start_x, start_y = start
    end_x, end_y = end

    diff_x = end_x - start_x
    diff_y = end_y - start_y

    sign_x = int(diff_x / abs(diff_x)) if diff_x != 0 else 0
    sign_y = int(diff_y / abs(diff_y)) if diff_y != 0 else 0

    range_x = (
        range(start_x, end_x + sign_x, sign_x)
        if sign_x != 0
        else range(start_x, end_x)
    )
    range_y = (
        range(start_y, end_y + sign_y, sign_y)
        if sign_y != 0
        else range(start_y, end_y)
    )

    if diff_x == 0:
        for y in range_y:
            atlas[(start_x, y)] += 1
    elif diff_y == 0:
        for x in range_x:
            atlas[(x, start_y)] += 1
    elif abs(diff_x) == abs(diff_y):
        for x, y in zip(range_x, range_y):
            atlas[(x, y)] += 1
    else:
        pass


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        lines = [parse_line(raw_line) for raw_line in f.readlines()]

    min_x, min_y = 0, 0
    max_x = max(max(line[0][0], line[1][0]) for line in lines)
    max_y = max(max(line[0][1], line[1][1]) for line in lines)

    atlas = make_atlas((min_x, min_y), (max_x, max_y))
    for line in lines:
        add_ver_hor_line_to_atlas(atlas, line)

    answer_1 = sum(1 for value in atlas.values() if value > 1)
    assert answer_1 == 5835
    print(answer_1)

    atlas = make_atlas((min_x, min_y), (max_x, max_y))
    for line in lines:
        add_ver_hor_diag_line_to_atlas(atlas, line)

    answer_2 = sum(1 for value in atlas.values() if value > 1)
    assert answer_2 == 17013
    print(answer_2)


if __name__ == "__main__":
    main()
