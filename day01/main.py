from itertools import islice, tee
from typing import Iterable, Iterator
import os.path

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


def diffs(xs: Iterable[int]) -> Iterator[int]:
    lefts, rights = tee(xs)
    yield from (
        right - left
        for left, right in zip(lefts, islice(rights, 1, None))
    )


def triads(xs: Iterable[int]) -> Iterator[int]:
    lefts, middles, rights = tee(xs, 3)
    yield from (
        left + middle + right
        for left, middle, right in zip(
            lefts, islice(middles, 1, None), islice(rights, 2, None)
        )
    )


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        depths = [int(line) for line in f.readlines()]

    answer_1 = sum(1 for diff in diffs(depths) if diff > 0)
    assert answer_1 == 1390
    print(answer_1)

    answer_2 = sum(1 for diff in diffs(triads(depths)) if diff > 0)
    print(answer_2)


if __name__ == "__main__":
    main()
