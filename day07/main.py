from statistics import median
import os.path

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


def parse_positions(raw_timer_list: str) -> list[int]:
    return [int(timer) for timer in raw_timer_list.strip().split(',')]


def triangular(n: int) -> int:
    return n * (n + 1) // 2


def linear_fuel_cost(positions: list[int], position: int) -> int:
    return sum(abs(position - p) for p in positions)


def triangular_fuel_cost(positions: list[int], position: int) -> int:
    return sum(triangular(abs(position - p)) for p in positions)


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        raw_positions = f.read()
    positions = parse_positions(raw_positions)

    best_position = int(median(positions))
    answer_1 = linear_fuel_cost(positions, best_position)
    assert answer_1 == 341558
    print(answer_1)

    answer_2 = min(triangular_fuel_cost(positions, p) for p in set(positions))
    assert answer_2 == 93214037
    print(answer_2)


if __name__ == "__main__":
    main()
