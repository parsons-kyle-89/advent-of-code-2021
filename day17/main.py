from dataclasses import dataclass
import os.path
import re
from typing import Iterator

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


Trajectory = Iterator[tuple[int, int]]


@dataclass(frozen=True)
class Target:
    left: int
    right: int
    bottom: int
    top: int

    def __contains__(self, point: tuple[int, int]) -> bool:
        x, y = point
        return self.left <= x <= self.right and self.bottom <= y <= self.top


def parse_target(raw_target: str) -> Target:
    left, right, bottom, top = re.findall(r'[-\d]+', raw_target)
    return Target(int(left), int(right), int(bottom), int(top))


def sign(a: int) -> int:
    if a < 0:
        return -1
    elif a > 0:
        return 1
    else:
        return 0


def naturals() -> Iterator[int]:
    i = 0
    while True:
        yield i
        i += 1


def tri(n: int) -> int:
    return n * (n + 1) // 2


def trajectory(v_x: int, v_y: int) -> Trajectory:
    x, y = 0, 0
    while True:
        x += v_x
        y += v_y
        v_x -= sign(v_x)
        v_y -= 1
        yield x, y


def trajectory_hits_target(trajectory: Trajectory, target: Target) -> bool:
    for x, y in trajectory:
        if (x, y) in target:
            return True
        elif y < target.bottom:
            return False
    raise RuntimeError


def aim(target: Target) -> tuple[int, int]:
    v_x = next(v for v in naturals() if target.left <= tri(v) <= target.right)
    for v_y in range(-target.bottom, 0, -1):
        if trajectory_hits_target(trajectory(v_x, v_y), target):
            return v_x, v_y
    raise RuntimeError


def max_y(trajectory: Trajectory) -> int:
    _, now_seen = next(trajectory)
    while True:
        _, next_seen = next(trajectory)
        if next_seen < now_seen:
            return now_seen
        now_seen = next_seen


def find_trajectories(target: Target) -> list[tuple[int, int]]:
    return [
        (v_x, v_y)
        for v_x in range(0, target.right + 2)
        for v_y in range(target.bottom - 2, -target.bottom + 2)
        if trajectory_hits_target(trajectory(v_x, v_y), target)
    ]


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        raw_target = f.read()
    target = parse_target(raw_target)
    v_x, v_y = aim(target)

    answer_1 = max_y(trajectory(v_x, v_y))
    assert answer_1 == 4186
    print(answer_1)

    answer_2 = len(find_trajectories(target))
    assert answer_2 == 2709
    print(answer_2)


if __name__ == "__main__":
    main()
