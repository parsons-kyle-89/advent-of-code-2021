from collections import Counter
from operator import itemgetter
import os.path
from typing import Callable, Iterable, Tuple, TypeVar

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))

A = TypeVar('A')


def _common(  # type: ignore[misc]
    iterable: Iterable[A],
    func: Callable[..., Tuple[A, int]],
) -> A:
    count = Counter(iterable)
    return func(count.items(), key=itemgetter(1, 0))[0]


def most_common(iterable: Iterable[A]) -> A:
    return _common(iterable, max)


def least_common(iterable: Iterable[A]) -> A:
    return _common(iterable, min)


def filter_lines(
    lines: Iterable[str],
    criterion: Callable[[Iterable[str]], str],
) -> str:
    i = 0
    while True:
        idx_criterion = criterion(line[i] for line in lines)
        lines = [
            line for line in lines
            if line[i] == idx_criterion
        ]
        if len(lines) == 1:
            return lines[0]
        i += 1


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    gamma = int(''.join(most_common(digit) for digit in zip(*lines)), base=2)
    epsilon = 2 ** len(lines[0]) - 1 - gamma

    answer_1 = gamma * epsilon
    assert answer_1 == 4006064
    print(answer_1)

    co2_rating = int(filter_lines(lines, most_common), base=2)
    o2_rating = int(filter_lines(lines, least_common), base=2)

    answer_2 = co2_rating * o2_rating
    assert answer_2 == 5941884
    print(answer_2)


if __name__ == "__main__":
    main()
