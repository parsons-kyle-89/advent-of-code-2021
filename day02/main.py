import os.path

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        moves = f.readlines()

    horiz, depth = 0, 0
    for move in moves:
        direction, distance = move.split(maxsplit=1)
        distance = int(distance)
        match direction:
            case 'forward':
                horiz += distance
            case 'up':
                depth -= distance
            case 'down':
                depth += distance

    answer_1 = horiz * depth
    assert answer_1 == 1690020
    print(answer_1)

    horiz, depth, aim = 0, 0, 0
    for move in moves:
        direction, distance = move.split(maxsplit=1)
        distance = int(distance)
        match direction:
            case 'forward':
                horiz += distance
                depth += distance * aim
            case 'up':
                aim -= distance
            case 'down':
                aim += distance

    answer_2 = horiz * depth
    assert answer_2 == 1408487760
    print(answer_2)


if __name__ == "__main__":
    main()
