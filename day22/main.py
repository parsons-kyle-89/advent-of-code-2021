from collections import defaultdict
from dataclasses import dataclass
from itertools import pairwise
import os.path

from pprint import pprint
from tqdm import tqdm

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


@dataclass(frozen=True)
class Cube:
    x_min: int
    y_min: int
    z_min: int
    x_max: int
    y_max: int
    z_max: int

    def __contains__(self, other: "Cube") -> bool:
        return (
            self.x_min <= other.x_min and other.x_max <= self.x_max
            and self.y_min <= other.y_min and other.y_max <= self.y_max
            and self.z_min <= other.z_min and other.z_max <= self.z_max
        )

    def size(self) -> int:
        return (self.x_max - self.x_min) * (self.y_max - self.y_min) * (self.z_max - self.z_min)

    def intersects(self, other: "Cube") -> bool:
        x0 = max(self.x_min, other.x_min)
        y0 = max(self.y_min, other.y_min)
        z0 = max(self.z_min, other.z_min)
        x1 = min(self.x_max, other.x_max)
        y1 = min(self.y_max, other.y_max)
        z1 = min(self.z_max, other.z_max)
        return (x0 < x1) and (y0 < y1) and (z0 < z1)

    def intersections(self, other: "Cube") -> list["Cube"]:
        in_others = []
        xs = sorted([self.x_min, self.x_max, other.x_min, other.x_max])
        ys = sorted([self.y_min, self.y_max, other.y_min, other.y_max])
        zs = sorted([self.z_min, self.z_max, other.z_min, other.z_max])
        for x0, x1 in pairwise(xs):
            for y0, y1 in pairwise(ys):
                for z0, z1 in pairwise(zs):
                    sub_cube = Cube(x0, y0, z0, x1, y1, z1)
                    if sub_cube in other and sub_cube not in self:
                        in_others.append(sub_cube)
        return in_others


@dataclass(frozen=True)
class Instruction:
    cube: Cube
    state: int


# @dataclass
# class Grid:
#     cubes: set[Cube]
# 
#     def __setitem__(self, cube: Cube, value: int) -> None:
#         intersecting_cubes = [current_cube for current_cube in self.cubes if current_cube.intersects(cube) and current_cube not in cube]
#         non_intersecting_cubes = {current_cube for current_cube in self.cubes if not current_cube.intersects(cube)}
#         new_cubes = non_intersecting_cubes
# 
#         for intersecting_cube in intersecting_cubes:
#             intersections = cube.intersections(intersecting_cube)
#             new_cubes.update(intersections)
#         
#         if value:
#             new_cubes.add(cube)
# 
#         self.cubes = new_cubes


def parse_instruction(raw_instruction: str) -> Instruction:
    state, ranges = raw_instruction.strip().split(' ', maxsplit=1)
    state = 1 if state=='on' else 0

    x_range, y_range, z_range = ranges.split(',', maxsplit=2)
    x_min, x_max = parse_range(x_range)
    y_min, y_max = parse_range(y_range)
    z_min, z_max = parse_range(z_range)

    return Instruction(
        Cube(x_min, y_min, z_min, x_max, y_max, z_max),
        state,
    )


def parse_range(raw_range: str) -> tuple[int, int]:
    start, stop = raw_range.lstrip('xyz=').split('..', maxsplit=1)
    return int(start), int(stop) + 1


def apply_instruction(cubes: set[Cube], instruction: Instruction) -> None:
    new_cube = instruction.cube
    value = instruction.state

    intersecting_cubes = [current_cube for current_cube in cubes if current_cube.intersects(new_cube) and current_cube not in new_cube]
    non_intersecting_cubes = {current_cube for current_cube in cubes if not current_cube.intersects(new_cube)}
    new_cubes = non_intersecting_cubes

    for intersecting_cube in intersecting_cubes:
        intersections = new_cube.intersections(intersecting_cube)
        new_cubes.update(intersections)
    
    if value:
        new_cubes.add(new_cube)

    return new_cubes


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        raw_instructions = f.readlines()
    instructions = [parse_instruction(raw_instruction) for raw_instruction in raw_instructions]
    cubes = set()

    for instruction in tqdm(instructions[:20]):
        cubes = apply_instruction(cubes, instruction)

    answer_1 = sum(cube.size() for cube in cubes)
    assert answer_1 == 551693
    print(answer_1)

    for instruction in tqdm(instructions[20:]):
        cubes = apply_instruction(cubes, instruction)

    answer_2 = sum(cube.size() for cube in cubes)
    assert answer_2 == 1165737675582132
    print(answer_2)

    # ins1 = Instruction(Cube(0, 0, 0, 3, 3, 3), 0)
    # ins2 = Instruction(Cube(1, 1, 1, 5, 5, 5), e)
    # grid = Grid({})
    # apply_instruction(grid, ins1)
    # apply_instruction(grid, ins2)
    # pprint(grid)
    # cube1 = Cube(0, 0, 0, 1, 1, 1)
    # cube2 = Cube(2, 2, 2, 3, 3, 3)
    # cube3 = Cube(1, 1, 1, 4, 4, 4)
    # cube4 = Cube(2, 2, 2, 5, 5, 5)
    # pprint(cube4.intersections([cube3]))
    # print(cube1.intersects(cube2))
    # print(cube2.intersects(cube1))
    # print(cube3.intersects(cube2))
    # print(cube2.intersects(cube3))
    # print(cube1.intersects(cube1))


if __name__ == "__main__":
    main()
