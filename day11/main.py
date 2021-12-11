import numpy as np
import numpy.typing as np_typing
import os.path
from scipy.ndimage import convolve

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))
NEIGHBOR_KERNEL = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])

Grid = np_typing.NDArray[np.int64]


def parse_row(raw_row: str) -> list[int]:
    return [int(cell) for cell in raw_row]


def simulate_step(grid: Grid) -> tuple[Grid, int]:
    new_grid = grid.copy()
    new_grid += 1

    flash = new_grid >= 10
    ever_flash = flash.copy()
    while np.any(flash):
        new_grid += convolve(
            flash.astype(int), NEIGHBOR_KERNEL, mode='constant'
        )
        flash = (new_grid >= 10) & ~ever_flash
        ever_flash |= flash
    new_grid[ever_flash] = 0

    return new_grid, np.sum(ever_flash)


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        raw_rows = f.readlines()
    rows = [parse_row(raw_row.strip()) for raw_row in raw_rows]
    grid = np.array(rows)

    flashes = 0
    for _ in range(100):
        grid, new_flashes = simulate_step(grid)
        flashes += new_flashes

    answer_1 = flashes
    assert answer_1 == 1757
    print(answer_1)

    round_count = 100
    while np.sum(grid) > 0:
        grid, _ = simulate_step(grid)
        round_count += 1

    answer_2 = round_count
    # assert answer_2 == 'there\n'
    print(answer_2)


if __name__ == "__main__":
    main()
