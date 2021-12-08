from dataclasses import dataclass
import os.path

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


Digit = set[str]


@dataclass
class DisplayEntry:
    digits: list[Digit]
    output: list[Digit]


def parse_display_entry(raw_display_entry: str) -> DisplayEntry:
    raw_digits, raw_output = raw_display_entry.split('|')
    digits = [set(digit.strip()) for digit in raw_digits.split()]
    output = [set(digit.strip()) for digit in raw_output.split()]
    return DisplayEntry(digits, output)


def identify_digit(digit: Digit, digits: list[Digit]) -> str:
    if len(digit) == 2:
        return '1'
    elif len(digit) == 3:
        return '7'
    elif len(digit) == 4:
        return '4'
    elif len(digit) == 7:
        return '8'
    elif len(digit) == 5:
        up_set_size = sum(1 for d in digits if digit < d)
        if up_set_size == 1:
            return '2'
        elif up_set_size == 2:
            return '3'
        elif up_set_size == 3:
            return '5'
        else:
            raise ValueError
    elif len(digit) == 6:
        down_set_size = sum(1 for d in digits if d < digit)
        if down_set_size == 1:
            return '6'
        elif down_set_size == 2:
            return '0'
        elif down_set_size == 5:
            return '9'
        else:
            raise ValueError
    else:
        raise ValueError


def identify_output(display_entry: DisplayEntry) -> int:
    digits = display_entry.digits
    output = display_entry.output
    return int(''.join(identify_digit(d, digits) for d in output))


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        display_entries = [
            parse_display_entry(raw_display_entry)
            for raw_display_entry in f.readlines()
        ]

    answer_1 = sum(
        1
        for display_entry in display_entries
        for digit in display_entry.output
        if len(digit) in (2, 3, 4, 7)
    )
    assert answer_1 == 383
    print(answer_1)

    answer_2 = sum(
        identify_output(display_entry)
        for display_entry in display_entries
    )
    assert answer_2 == 998900
    print(answer_2)


if __name__ == "__main__":
    main()
