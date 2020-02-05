import asyncio
from itertools import chain
from itertools import cycle
from itertools import repeat
from os import path
from typing import Iterator
from typing import List

BASE_PATTERN = [0, 1, 0, -1]


def pattern_for_idx(idx: int) -> Iterator[int]:
    idx_pattern = [repeat(p, idx + 1) for p in BASE_PATTERN]
    ret = cycle(chain(*idx_pattern))
    next(ret)  # Always remove the first value from the pattern
    return ret


def calc_value(data: List[int], idx: int) -> int:
    params = zip(data, pattern_for_idx(idx))
    ret = sum(val * pattern for val, pattern in params)
    ret = abs(ret) % 10
    return ret


def process_transmission(data: List[int], phases: int = 100) -> List[int]:
    for _ in range(phases):
        data = [calc_value(data, idx) for idx, _ in enumerate(data)]
    return data


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, 'input.txt')
    with open(infile, 'r') as input_file:
        data = [int(c) for c in input_file.read().strip()]
        output = process_transmission(data)
        solution = ''.join(str(v) for v in output[:8])
        print(f'Solution: {solution}')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
