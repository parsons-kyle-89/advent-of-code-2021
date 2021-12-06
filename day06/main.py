from collections import Counter
import os.path

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


def parse_timer_list(raw_timer_list: str) -> list[int]:
    return [int(timer) for timer in raw_timer_list.strip().split(',')]


def make_timers(timer_list: list[int]) -> dict[int, int]:
    return dict(Counter(timer_list))


def tick_timers(timers: dict[int, int]) -> dict[int, int]:
    new_timers = {
        day - 1: count
        for day, count in timers.items()
        if day > 0
    }
    new_timers[6] = timers.get(0, 0) + new_timers.get(6, 0)
    new_timers[8] = timers.get(0, 0)
    return new_timers


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        raw_timer_list = f.read()
    timer_list = parse_timer_list(raw_timer_list)
    timers = make_timers(timer_list)

    for _ in range(80):
        timers = tick_timers(timers)

    answer_1 = sum(timers.values())
    assert answer_1 == 362639
    print(answer_1)

    for _ in range(256 - 80):
        timers = tick_timers(timers)

    answer_2 = sum(timers.values())
    assert answer_2 == 1639854996917
    print(answer_2)


if __name__ == "__main__":
    main()
