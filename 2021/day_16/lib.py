from collections.abc import Callable
from typing import Union


class Packet:
    def __init__(self, version: int, type: int, data: Union[int, list["Packet"]]) -> None:
        self.version = version
        self.type = type
        self.data = data


def bitstream(data: str) -> Callable[[int], str]:
    stream = (c for i in range(0, len(data), 2) for c in f"{int(data[i:i+2], 16):08b}")

    def _helper(n: int) -> str:
        return "".join(next(stream) for _ in range(n))

    return _helper


def parse_packet(data: Callable[[int], str]) -> tuple[Packet, int]:
    version = int(data(3), 2)
    packet_type = int(data(3), 2)
    bits_consumed = 6

    if packet_type == 4:
        # Literal value
        continue_flag = "1"
        num = ""
        while continue_flag == "1":
            continue_flag = data(1)
            num += data(4)
            bits_consumed += 5

        return Packet(version, packet_type, int(num, 2)), bits_consumed

    subpackets: list[Packet] = []
    subpacket_bits_consumed = 0

    len_type = data(1)
    bits_consumed += 1

    if len_type == "0":
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
