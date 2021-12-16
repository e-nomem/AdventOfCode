import asyncio
from os import path
from typing import Callable
from typing import Union

from lib.timing import benchmark

# Can't be bothered to figure out the zero padding right now
HEX_MAP = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}


class Packet:
    def __init__(self, version: int, type: int, data: Union[int, list['Packet']]) -> None:
        self.version = version
        self.type = type
        self.data = data


def parse_packet(data: Callable[[int], str]) -> tuple[Packet, int]:
    version = int(data(3), 2)
    packet_type = int(data(3), 2)
    bits_consumed = 6

    if packet_type == 4:
        # Literal value
        continue_flag = '1'
        num = ''
        while continue_flag == '1':
            continue_flag = data(1)
            num += data(4)
            bits_consumed += 5

        return Packet(version, packet_type, int(num, 2)), bits_consumed

    subpackets: list[Packet] = []
    subpacket_bits_consumed = 0

    len_type = data(1)
    bits_consumed += 1

    if len_type == '0':
        # 15 bits of len data
        subpacket_len = int(data(15), 2)
        bits_consumed += 15
        has_subpackets = lambda: subpacket_bits_consumed < subpacket_len
    else:
        # 11 bits of packet count
        subpacket_count = int(data(11), 2)
        bits_consumed += 11
        has_subpackets = lambda: len(subpackets) < subpacket_count

    while has_subpackets():
        packet, consumed = parse_packet(data)
        subpackets.append(packet)
        subpacket_bits_consumed += consumed

    return Packet(version, packet_type, subpackets), bits_consumed + subpacket_bits_consumed


def sum_versions(packet: Packet) -> int:
    if isinstance(packet.data, int):
        # Only happens for type 4 'literal' packets
        return packet.version

    return sum(sum_versions(p) for p in packet.data) + packet.version


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    data = input_lines[0].strip()
    bitstream = (b for c in data for b in HEX_MAP[c])

    def read(n: int) -> str:
        return ''.join(next(bitstream) for _ in range(n))

    packet, _ = parse_packet(read)

    # Sanity check that we processed all the data
    remaining_data = [b for b in bitstream]
    assert int(''.join(remaining_data), 2) == 0, 'Leftover data should only be zero padding, found actual data'
    assert len(remaining_data) < 8, f'There should be less than 1 byte of zero padding at the end, found {len(remaining_data)} bits'

    print(sum_versions(packet))


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, 'input.txt')
    with open(infile) as input_file:
        input_lines = [l for l in input_file]

    puzzle(input_lines)


if __name__ == '__main__':
    asyncio.run(main())
