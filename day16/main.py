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
    value: int


@dataclass(frozen=True)
class Sum:
    version: int
    operands: list["Packet"]


@dataclass(frozen=True)
class Product:
    version: int
    operands: list["Packet"]


@dataclass(frozen=True)
class Min:
    version: int
    operands: list["Packet"]


@dataclass(frozen=True)
class Max:
    version: int
    operands: list["Packet"]


@dataclass(frozen=True)
class GreaterThan:
    version: int
    left: "Packet"
    right: "Packet"


@dataclass(frozen=True)
class LessThan:
    version: int
    left: "Packet"
    right: "Packet"


@dataclass(frozen=True)
class EqualTo:
    version: int
    left: "Packet"
    right: "Packet"


Packet = (
    Literal
    | Sum
    | Product
    | Min
    | Max
    | GreaterThan
    | LessThan
    | EqualTo
)
PACKET_TYPE = {
    0: Sum,
    1: Product,
    2: Min,
    3: Max,
    4: Literal,
    5: GreaterThan,
    6: LessThan,
    7: EqualTo,
}


def parse_bit_queue(bit_queue: BitQueue) -> tuple[Packet, int]:
    already_consumed = bit_queue.consumed

    version = bit_queue.take(3)
    type_id = bit_queue.take(3)

    if type_id == 4:
        value = 0
        while bit_queue.take(1) == 1:
            value = value * 16 + bit_queue.take(4)
        value = value * 16 + bit_queue.take(4)
        packet = Literal(version, value)

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

        packet_type = PACKET_TYPE[type_id]
        if packet_type in (GreaterThan, LessThan, EqualTo):
            left, right = subpackets
            packet = packet_type(version, left, right)
        elif packet_type in (Sum, Product, Min, Max):
            packet = packet_type(version, subpackets)

    return packet, bit_queue.consumed - already_consumed


def hex_to_bin(hex_packet: str) -> str:
    return ''.join(f"{int(digit, base=16):04b}" for digit in hex_packet)


def sum_versions(packet: Packet) -> int:
    if isinstance(packet, Literal):
        return packet.version
    elif isinstance(packet, (Sum, Product, Min, Max)):
        return packet.version + sum(sum_versions(op) for op in packet.operands)
    elif isinstance(packet, (GreaterThan, LessThan, EqualTo)):
        return (
            packet.version
            + sum_versions(packet.left)
            + sum_versions(packet.right)
        )
    else:
        raise RuntimeError


def evaluate_packet(packet: Packet) -> int:
    match packet:
        case Literal(_, value):
            return value
        case Sum(_, summands):
            return sum(evaluate_packet(summand) for summand in summands)
        case Product(_, factors):
            value = 1
            for factor in factors:
                value *= evaluate_packet(factor)
            return value
        case Min(_, operands):
            return min(evaluate_packet(operand) for operand in operands)
        case Max(_, operands):
            return max(evaluate_packet(operand) for operand in operands)
        case GreaterThan(_, left, right):
            return 1 if evaluate_packet(left) > evaluate_packet(right) else 0
        case LessThan(_, left, right):
            return 1 if evaluate_packet(left) < evaluate_packet(right) else 0
        case EqualTo(_, left, right):
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
