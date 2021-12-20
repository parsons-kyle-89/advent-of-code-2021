from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations
import os.path

import numpy as np
import numpy.typing as np_typing

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


FACINGS = [
    np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ]),
    np.array([
        [0, -1, 0],
        [1, 0, 0],
        [0, 0, 1],
    ]),
    np.array([
        [-1, 0, 0],
        [0, -1, 0],
        [0, 0, 1],
    ]),
    np.array([
        [0, 1, 0],
        [-1, 0, 0],
        [0, 0, 1],
    ]),
    np.array([
        [0, 0, 1],
        [0, 1, 0],
        [-1, 0, 0],
    ]),
    np.array([
        [0, 0, -1],
        [0, 1, 0],
        [1, 0, 0],
    ]),
]
ROTATIONS = [
    np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ]),
    np.array([
        [1, 0, 0],
        [0, 0, -1],
        [0, 1, 0],
    ]),
    np.array([
        [1, 0, 0],
        [0, -1, 0],
        [0, 0, -1],
    ]),
    np.array([
        [1, 0, 0],
        [0, 0, 1],
        [0, -1, 0],
    ]),
]


@dataclass
class Scanner:
    number: int
    beacon_locs: np_typing.NDArray[np.int64]
    pairwise_distances: np_typing.NDArray[np.int64]


def parse_scanner(raw_scanner: str) -> Scanner:
    header, body = raw_scanner.split('\n', maxsplit=1)
    scanner_number = int(
        header
        .removeprefix('--- scanner ')
        .removesuffix(' ---')
    )
    beacon_locs = np.array([
        parse_beacon(raw_beacon) for raw_beacon in body.splitlines()
    ])
    distances = square_distances(beacon_locs)
    return Scanner(scanner_number, beacon_locs, distances)


def parse_beacon(raw_beacon: str) -> tuple[int, int, int]:
    x, y, z = raw_beacon.split(',')
    return int(x), int(y), int(z)


def square_distances(
    arr: np_typing.NDArray[np.int64]
) -> np_typing.NDArray[np.int64]:
    arr = np.reshape(arr, (-1, 1, 3))
    return np.sum((arr - np.swapaxes(arr, 0, 1)) ** 2, axis=-1)


def count_equal(
    arr1: np_typing.NDArray[np.int64],
    arr2: np_typing.NDArray[np.int64]
) -> np.int64:
    return np.sum(
        np.any(
            arr1.reshape(1, -1)
            ==
            arr2.reshape(-1, 1),
            axis=1
        )
    )


def calibrate(
    calib_i: np_typing.NDArray[np.int64],
    calib_j: np_typing.NDArray[np.int64]
) -> tuple[np_typing.NDArray[np.int64], np_typing.NDArray[np.int64]]:
    bottom_bounding_point_i = np.amin(calib_i, axis=0)
    for facing in FACINGS:
        for rotation in ROTATIONS:
            trans = facing @ rotation
            trans_j = calib_j @ trans
            bottom_bounding_point_j = np.amin(trans_j, axis=0)
            offset_ji = bottom_bounding_point_i - bottom_bounding_point_j
            trans_j = trans_j + offset_ji
            if np.all(trans_j == calib_i):
                return trans, offset_ji
    else:
        raise ValueError


def apply_calibration(
    beacons: np_typing.NDArray[np.int64],
    trans: np_typing.NDArray[np.int64],
    offset: np_typing.NDArray[np.int64]
) -> np_typing.NDArray[np.int64]:
    return beacons @ trans + offset


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        raw_scanners = f.read().split('\n\n')
    scanners = [
        parse_scanner(raw_scanner)
        for raw_scanner in raw_scanners
    ]

    matching_points_: defaultdict[tuple[int, int], list[tuple[int, int]]] = (
        defaultdict(list)
    )
    for scanner_i, scanner_j in combinations(scanners, 2):
        i, j = scanner_i.number, scanner_j.number
        dists_i = scanner_i.pairwise_distances
        dists_j = scanner_j.pairwise_distances
        for ii, i_row in enumerate(dists_i):
            for (jj, j_row) in enumerate(dists_j):
                if count_equal(i_row, j_row) >= 12:
                    matching_points_[(i, j)].append((ii, jj))
                    matching_points_[(j, i)].append((jj, ii))
    matching_points = {
        p: np.array(m) for p, m in matching_points_.items()
    }

    calibrated_offsets = {0: np.array([0, 0, 0])}
    while len(calibrated_offsets) != len(scanners):
        for (i, j), points in matching_points.items():
            if i in calibrated_offsets and j not in calibrated_offsets:
                scanner_j = scanners[j]
                calib_i = scanners[i].beacon_locs[points[:, 0]]
                calib_j = scanner_j.beacon_locs[points[:, 1]]

                trans, offset = calibrate(calib_i, calib_j)
                calibrated_j = apply_calibration(
                    scanner_j.beacon_locs, trans, offset
                )

                scanners[j] = Scanner(
                    scanner_j.number,
                    calibrated_j,
                    scanner_j.pairwise_distances
                )
                calibrated_offsets[j] = offset

    deduped_beacons = set.union(*[
        {tuple(beacon) for beacon in scanner.beacon_locs}
        for scanner in scanners
    ])

    answer_1 = len(deduped_beacons)
    assert answer_1 == 326
    print(answer_1)

    answer_2 = max(
        np.sum(np.abs(loc1 - loc2))
        for loc1, loc2 in combinations(calibrated_offsets.values(), 2)
    )
    assert answer_2 == 10630
    print(answer_2)


if __name__ == "__main__":
    main()
