import asyncio
from collections import Counter
from functools import cache
from itertools import product
from os import path
from typing import TypeVar

from lib.timing import benchmark

_T = TypeVar("_T")

ROLL_FREQUENCIES = Counter(sum(r) for r in product(range(1, 4), repeat=3))
POS_AND_ROLL = {(p, r): (p + r) % 10 for p in range(10) for r in ROLL_FREQUENCIES.keys()}
WIN_THRESHOLD = 21


def tuple_shift_left(t: tuple[_T, ...], val: _T) -> tuple[_T, ...]:
    return t[1:] + (val,)


@cache
def play_dirac(positions: tuple[int, ...], scores: tuple[int, ...] = None) -> tuple[int, ...]:
    if scores is None:
        scores = tuple(0 for _ in positions)

    wins = [0] * len(positions)

    for roll, freq in ROLL_FREQUENCIES.items():
        pos = POS_AND_ROLL[(positions[0], roll)]
        score = scores[0] + pos + 1

        if score >= WIN_THRESHOLD:
            wins[0] += freq
        else:
            recursive_wins = play_dirac(
                tuple_shift_left(positions, pos),
                tuple_shift_left(scores, score),
            )
            # Returned wins are rotated left by 1, so we need to rotate them back as we add them up
            wins = [w + (recursive_wins[i - 1] * freq) for i, w in enumerate(wins)]

    return tuple(wins)


@benchmark(10, cleanup=lambda: play_dirac.cache_clear())
def puzzle(input_lines: list[str]) -> None:
    positions = tuple(int(l.strip().split(": ")[1]) - 1 for l in input_lines)
    print(max(play_dirac(positions)))


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
