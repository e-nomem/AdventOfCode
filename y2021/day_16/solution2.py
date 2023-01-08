import asyncio
from collections.abc import Callable
from functools import reduce
from operator import add
from operator import eq
from operator import gt
from operator import lt
from operator import mul
from os import path

from .lib import bitstream
from .lib import Packet
from .lib import parse_packet
from aoclib.timing import benchmark

OPERATORS: list[Callable[[int, int], int]] = [
    add,
    mul,
    min,
    max,
    lambda a, i: i,  # Unused, here to make sure the indexes match
    gt,
    lt,
    eq,
]


def process_packet(packet: Packet) -> int:
    if isinstance(packet.data, int):
        # Only happens for type 4 'literal' packets
        return packet.data

    return int(reduce(OPERATORS[packet.type], (process_packet(p) for p in packet.data)))


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    data = bitstream(input_lines[0].strip())
    packet, _ = parse_packet(data)

    print(process_packet(packet))


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
