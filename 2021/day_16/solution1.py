import asyncio
from os import path
from typing import Callable
from typing import Union

from .lib import bitstream
from .lib import Packet
from .lib import parse_packet
from lib.timing import benchmark


def sum_versions(packet: Packet) -> int:
    if isinstance(packet.data, int):
        # Only happens for type 4 'literal' packets
        return packet.version

    return sum(sum_versions(p) for p in packet.data) + packet.version


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    data = bitstream(input_lines[0].strip())
    packet, _ = parse_packet(data)

    print(sum_versions(packet))


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, 'input.txt')
    with open(infile) as input_file:
        input_lines = [l for l in input_file]

    puzzle(input_lines)


if __name__ == '__main__':
    asyncio.run(main())
