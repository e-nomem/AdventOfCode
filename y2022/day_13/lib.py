from enum import Enum

PPart = int | list["PPart"]


class Result(int, Enum):
    Ordered = -1
    Continue = 0
    Unordered = 1


def _parse_packet_helper(inp: str) -> tuple[PPart, int]:
    parts = []
    consumed = 0
    idx = 0
    while consumed < len(inp):
        while inp[idx] not in {"[", "]", ","}:
            idx += 1

        match inp[idx]:
            case "[":
                recursive_part, recursive_consumed = _parse_packet_helper(inp[idx + 1 :])
                parts.append(recursive_part)
                consumed += recursive_consumed
                idx = consumed
            case sym:
                if idx != consumed:
                    val = int(inp[consumed:idx])
                    parts.append(val)

                idx += 1
                consumed = idx

                if sym == "]":
                    return parts, consumed + 1


def parse_packet(line: str) -> PPart:
    return _parse_packet_helper(line[1:])[0]


def is_ordered(left: PPart, right: PPart) -> Result:
    match isinstance(left, int), isinstance(right, int):
        case True, True:
            if left < right:
                return Result.Ordered
            elif left == right:
                return Result.Continue
            else:
                return Result.Unordered
        case True, False:
            return is_ordered([left], right)
        case False, True:
            return is_ordered(left, [right])

    for idx in range(len(left)):
        if idx == len(right):
            return Result.Unordered

        res = is_ordered(left[idx], right[idx])
        if res is not Result.Continue:
            return res

    if len(left) < len(right):
        return Result.Ordered

    return Result.Continue
