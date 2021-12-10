from dataclasses import dataclass
import os.path
from statistics import median
from typing import NoReturn

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))

OPEN_CHARS = '({[<'
CLOSE_CHARS = ')}]>'
CLOSING_MATCH = {
    '(': ')',
    '{': '}',
    '[': ']',
    '<': '>',
}
ERROR_CHAR_SCORE = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}
COMPLETION_CHAR_SCORE = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


def absurd(x: NoReturn) -> NoReturn:
    raise RuntimeError


@dataclass
class ErrorChar:
    char: str


@dataclass
class IncompleteStack:
    stack: str


def try_parse(line: str) -> ErrorChar | IncompleteStack:
    char_stack = []
    for char in line:
        if char in OPEN_CHARS:
            char_stack.append(char)
        elif char in CLOSE_CHARS:
            if not char_stack:
                return ErrorChar(char)
            elif char == CLOSING_MATCH.get(char_stack[-1], ''):
                char_stack.pop(-1)
            else:
                return ErrorChar(char)
    return IncompleteStack(''.join(char_stack))


def completion_line(incomplete_stack: str) -> str:
    return ''.join(CLOSING_MATCH[char] for char in reversed(incomplete_stack))


def completion_line_score(completion_line: str) -> int:
    score = 0
    for char in completion_line:
        score *= 5
        score += COMPLETION_CHAR_SCORE[char]
    return score


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        lines = f.readlines()

    parse_results = (try_parse(line.strip()) for line in lines)
    error_chars = []
    incomplete_stacks = []
    for parse_result in parse_results:
        if isinstance(parse_result, ErrorChar):
            error_chars.append(parse_result.char)
        elif isinstance(parse_result, IncompleteStack):
            incomplete_stacks.append(parse_result.stack)
        else:
            absurd(parse_result)
    answer_1 = sum(ERROR_CHAR_SCORE.get(char, 0) for char in error_chars)

    assert answer_1 == 240123
    print(answer_1)

    completion_lines = [completion_line(stack) for stack in incomplete_stacks]
    completion_scores = [completion_line_score(li) for li in completion_lines]
    answer_2 = median(completion_scores)

    assert answer_2 == 3260812321
    print(answer_2)


if __name__ == "__main__":
    main()
