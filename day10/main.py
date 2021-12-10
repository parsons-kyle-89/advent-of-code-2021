from statistics import median
import os.path
from typing import NewType

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))

OPEN_CHARS = '({[<'
CLOSE_CHARS = ')}]>'
CLOSING_MATCH = {
    '(': ')',
    '{': '}',
    '[': ']',
    '<': '>',
}
CHAR_SCORE = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}
CHAR_SCORE_2 = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


ErrorChar = NewType('ErrorChar', str)
IncompleteStack = NewType('IncompleteStack', str)


def error_char(line):
    char_stack = []
    for char in line:
        if char in OPEN_CHARS:
            char_stack.append(char)
        elif char in CLOSE_CHARS:
            if not char_stack:
                return char, ''
            elif char == CLOSING_MATCH.get(char_stack[-1], ''):
                char_stack.pop(-1)
            else:
                return char, ''
    return '', ''.join(char_stack)


def completion_line(incomplete_stack):
    return ''.join(CLOSING_MATCH[char] for char in reversed(incomplete_stack))


def completion_line_score(completion_line):
    score = 0
    for char in completion_line:
        score *= 5
        score += CHAR_SCORE_2[char]
    return score


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        lines = f.readlines()

    error_chars, incomplete_stacks = zip(*list(error_char(line.strip()) for line in lines))
    answer_1 = sum(CHAR_SCORE.get(char, 0) for char in error_chars)

    assert answer_1 == 240123

    completion_lines = [completion_line(char_stack) for char_stack in incomplete_stacks if char_stack]
    completion_scores = [completion_line_score(line) for line in completion_lines]
    answer_2 = median(completion_scores)

    # assert answer_2 == 'there\n'
    print(answer_2)


if __name__ == "__main__":
    main()
