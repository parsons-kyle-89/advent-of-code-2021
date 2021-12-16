from dataclasses import dataclass
from enum import Enum
import os.path

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


@dataclass
class BitQueue:
    data: str
    consumed: int = 0

    def take(self, n: int) -> str:
        taken = self.data[:n]
        self.data = self.data[n:]
        self.consumed += n
        return int(taken, base=2)


class PacketType(Enum):
    SUM = 0
    PRODUCT = 1
    MIN = 2
    MAX = 3
    LITERAL = 4
    GREATER_THAN = 5
    LESS_THAN = 6
    EQUAL_TO = 7


@dataclass(frozen=True)
class Literal:
    version: int
    type_id: PacketType
    value: int


@dataclass(frozen=True)
class Operator:
    version: int
    type_id: PacketType
    packets: list["Packet"]


Packet = Literal | Operator


def parse_bit_queue(bit_queue: BitQueue) -> tuple[Packet, int]:
    already_consumed = bit_queue.consumed

    version = bit_queue.take(3)
    type_id = PacketType(bit_queue.take(3))

    if type_id == PacketType.LITERAL:
        value = 0
        while bit_queue.take(1) == 1:
            value = value * 16 + bit_queue.take(4)
        value = value * 16 + bit_queue.take(4)
        packet = Literal(version, type_id, value)

    else:
        length_type_id = bit_queue.take(1)
        if length_type_id == 0:
            bits_in_subpackets = bit_queue.take(15)
            bits_consumed = 0
            subpackets = []
            while bits_consumed < bits_in_subpackets:
                subpacket, subpacket_bits = parse_bit_queue(bit_queue)
                bits_consumed += subpacket_bits
                subpackets.append(subpacket)
        else:
            number_of_subpackets = bit_queue.take(11)
            subpackets = []
            for _ in range(number_of_subpackets):
                subpacket, _ = parse_bit_queue(bit_queue)
                subpackets.append(subpacket)
        packet = Operator(version, type_id, subpackets)

    return packet, bit_queue.consumed - already_consumed


def hex_to_bin(hex_packet: str) -> str:
    return ''.join(f"{int(digit, base=16):04b}" for digit in hex_packet)


def sum_versions(packet: Packet) -> int:
    match packet:
        case Literal(version, _, _):
            return version
        case Operator(version, _, subpackets):
            return version + sum(sum_versions(packet) for packet in subpackets)
        case _:
            raise RuntimeError


def evaluate_packet(packet: Packet) -> int:
    match packet:
        case Literal(_, _, value):
            return value
        case Operator(_, PacketType.SUM, packets):
            return sum(evaluate_packet(packet) for packet in packets)
        case Operator(_, PacketType.PRODUCT, packets):
            value = 1
            for packet in packets:
                value *= evaluate_packet(packet)
            return value
        case Operator(_, PacketType.MIN, packets):
            return min(evaluate_packet(packet) for packet in packets)
        case Operator(_, PacketType.MAX, packets):
            return max(evaluate_packet(packet) for packet in packets)
        case Operator(_, PacketType.GREATER_THAN, [left, right]):
            return 1 if evaluate_packet(left) > evaluate_packet(right) else 0
        case Operator(_, PacketType.LESS_THAN, [left, right]):
            return 1 if evaluate_packet(left) < evaluate_packet(right) else 0
        case Operator(_, PacketType.EQUAL_TO, [left, right]):
            return 1 if evaluate_packet(left) == evaluate_packet(right) else 0
        case _:
            raise RuntimeError


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        hex_packet = f.read().strip()
    bin_packet = hex_to_bin(hex_packet)
    packet, _ = parse_bit_queue(BitQueue(bin_packet))

    answer_1 = sum_versions(packet)
    assert answer_1 == 971
    print(answer_1)

    answer_2 = evaluate_packet(packet)
    assert answer_2 == 831996589851
    print(answer_2)


if __name__ == "__main__":
    main()
