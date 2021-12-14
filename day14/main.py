from collections import Counter, defaultdict
from dataclasses import dataclass
import os.path
from typing import Mapping

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


@dataclass(frozen=True)
class PairInsertionRule:
    pair: str
    insertion: str

    def new_pair_representation(self) -> tuple[str, str]:
        pair_l = self.pair[0]
        pair_r = self.pair[1]
        return pair_l + self.insertion, self.insertion + pair_r


def parse_raw_puzzle_input(
    raw_puzzle_input: str
) -> tuple[str, list[PairInsertionRule]]:
    template, pair_insertion_rules_chunk = (
        raw_puzzle_input.strip().split('\n\n', maxsplit=1)
    )
    pair_insertion_rules = [
        parse_pair_insertion_rule(raw_pair_insertion_rule)
        for raw_pair_insertion_rule in pair_insertion_rules_chunk.split('\n')
    ]
    return template, pair_insertion_rules


def parse_pair_insertion_rule(
    raw_pair_insertion_rule: str
) -> PairInsertionRule:
    pair, insertion = raw_pair_insertion_rule.split(' -> ')
    return PairInsertionRule(pair, insertion)


def count_pairs(template: str) -> defaultdict[str, int]:
    counts = Counter(template[i:i+2] for i in range(len(template) - 1))
    return defaultdict(int, counts)


def apply_pair_insertion_rules(
    pair_insertion_rules: list[PairInsertionRule],
    pair_counts: defaultdict[str, int]
) -> defaultdict[str, int]:
    new_pair_counts: defaultdict[str, int] = defaultdict(int)
    for rule in pair_insertion_rules:
        left_pair, right_pair = rule.new_pair_representation()
        new_pair_counts[left_pair] += pair_counts[rule.pair]
        new_pair_counts[right_pair] += pair_counts[rule.pair]
    return new_pair_counts


def count_elements(
    pair_counts: Mapping[str, int],
    first: str,
) -> defaultdict[str, int]:
    element_counts: defaultdict[str, int] = defaultdict(int)
    for pair, count in pair_counts.items():
        pair_r = pair[1]
        element_counts[pair_r] += count
    element_counts[first] += 1
    return element_counts


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        raw_puzzle_input = f.read()
    template, pair_insertion_rules = parse_raw_puzzle_input(raw_puzzle_input)
    pair_counts = count_pairs(template)
    for _ in range(10):
        pair_counts = apply_pair_insertion_rules(
            pair_insertion_rules, pair_counts
        )

    element_counts = count_elements(pair_counts, first=template[0])
    answer_1 = max(element_counts.values()) - min(element_counts.values())
    assert answer_1 == 4244
    print(answer_1)

    for _ in range(40 - 10):
        pair_counts = apply_pair_insertion_rules(
            pair_insertion_rules, pair_counts
        )

    element_counts = count_elements(pair_counts, first=template[0])
    answer_2 = max(element_counts.values()) - min(element_counts.values())
    assert answer_2 == 4807056953866
    print(answer_2)


if __name__ == "__main__":
    main()
