import os.path

import numpy as np
import numpy.typing as np_typing
from scipy.signal import convolve2d

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


CONV = np.array([
    [1, 2, 4],
    [8, 16, 32],
    [64, 128, 256],
])


def parse_algo(
    raw_algo: str
) -> tuple[np_typing.NDArray[np.int64], np_typing.NDArray[np.int64]]:
    raw_compression, raw_image = raw_algo.split('\n\n')
    compression = np.array([
        1 if char == '#' else 0
        for char in raw_compression
    ])
    image = np.array([
        [1 if char == '#' else 0 for char in row]
        for row in raw_image.splitlines()
    ])
    return compression, image


def enhance(
    image: np_typing.NDArray[np.int64],
    algo: np_typing.NDArray[np.int64],
    boundary: int
) -> np_typing.NDArray[np.int64]:
    enhanced = convolve2d(image, CONV, fillvalue=boundary)
    return algo[enhanced]


def show_image(image: np_typing.NDArray[np.int64]) -> str:
    return '\n'.join(
        ''.join('#' if pixel else '.' for pixel in row)
        for row in image
    )


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        raw_algo = f.read()
    algorithm, image = parse_algo(raw_algo)
    boundary_condition = algorithm[0]
    enhanced = enhance(
        enhance(image, algorithm, 0), algorithm, boundary_condition
    )

    answer_1 = np.sum(enhanced)
    assert answer_1 == 5306
    print(answer_1)

    for _ in range(24):
        enhanced = enhance(
            enhance(enhanced, algorithm, 0), algorithm, boundary_condition
        )

    answer_2 = np.sum(enhanced)
    assert answer_2 == 17497
    print(answer_2)


if __name__ == "__main__":
    main()
