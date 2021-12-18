from dataclasses import dataclass
from itertools import combinations
import os.path

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


@dataclass(frozen=True)
class Pair:
    left: "Surreal"
    right: "Surreal"

    def __str__(self) -> str:
        return '[' + str(self.left) + ',' + str(self.right) + ']'

    def __add__(self, other: "Surreal") -> "Pair":
        if isinstance(other, int):
            return Pair(self.left, self.right + other)
        return Pair(self, other)

    def __radd__(self, other: "Surreal") -> "Pair":
        return Pair(other + self.left, self.right)


Surreal = int | Pair


def parse_surreal(raw_surreal: str) -> Surreal:
    if raw_surreal.isnumeric() and raw_surreal.isascii():
        return int(raw_surreal)
    stripped = raw_surreal[1:-1]

    open_groups = 0
    for i, char in enumerate(stripped):
        if char == ',' and not open_groups:
            break

        if char == '[':
            open_groups += 1
        elif char == ']':
            open_groups -= 1

    return Pair(parse_surreal(stripped[:i]), parse_surreal(stripped[i+1:]))


def reduce(surreal: Surreal) -> Surreal:
    reduction = surreal
    while True:
        exploded = explode(reduction)
        if reduction != exploded:
            reduction = exploded
            continue

        splited = split(reduction)
        if reduction != splited:
            reduction = splited
            continue

        break
    return reduction


def explode(surreal: Surreal, depth: int = 4) -> Surreal:
    _, exploded, _, _ = _explode(surreal, depth)
    return exploded


def _explode(surreal: Surreal, depth: int) -> tuple[int, Surreal, int, bool]:
    if isinstance(surreal, int):
        return 0, surreal, 0, False

    if depth == 0:
        assert isinstance(surreal.left, int)
        assert isinstance(surreal.right, int)
        return surreal.left, 0, surreal.right, True

    left, center, right, did_explode = _explode(surreal.left, depth-1)
    if did_explode:
        return left, Pair(center, right + surreal.right), 0, True

    left, center, right, did_explode = _explode(surreal.right, depth-1)
    if did_explode:
        return 0, Pair(surreal.left + left, center), right, True

    return 0, surreal, 0, False


def split(surreal: Surreal) -> Surreal:
    split, _ = _split(surreal)
    return split


def _split(surreal: Surreal) -> tuple[Surreal, bool]:
    if isinstance(surreal, int):
        if surreal >= 10:
            left, right = surreal // 2, surreal // 2 + surreal % 2
            return Pair(left, right), True
        return surreal, False

    splited, did_split = _split(surreal.left)
    if did_split:
        return Pair(splited, surreal.right), True

    splited, did_split = _split(surreal.right)
    if did_split:
        return Pair(surreal.left, splited), True

    return surreal, False


def magnitude(surreal: Surreal) -> int:
    if isinstance(surreal, int):
        return surreal
    return 3 * magnitude(surreal.left) + 2 * magnitude(surreal.right)


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        raw_surreals = f.readlines()
    surreals = [
        parse_surreal(raw_surreal.strip())
        for raw_surreal in raw_surreals
    ]
    acc = surreals[0]
    for summand in surreals[1:]:
        acc += summand
        acc = reduce(acc)

    answer_1 = magnitude(acc)
    assert answer_1 == 3884
    print(answer_1)

    answer_2 = max(
        max(magnitude(reduce(x + y)), magnitude(reduce(y + x)))
        for x, y in combinations(surreals, 2)
    )
    assert answer_2 == 4595
    print(answer_2)


if __name__ == "__main__":
    main()
