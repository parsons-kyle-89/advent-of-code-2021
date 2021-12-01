import os.path

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        answer_1, answer_2 = f.readlines()

    assert answer_1 == 'hello\n'
    print(answer_1)

    assert answer_2 == 'there\n'
    print(answer_2)


if __name__ == "__main__":
    main()
