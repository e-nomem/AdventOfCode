import asyncio
from os import path

from aoclib.timing import benchmark


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    positions = [int(l.strip().split(": ")[1]) - 1 for l in input_lines]
    scores = [0] * len(positions)
    die = 0
    player = 0

    while all(s < 1000 for s in scores):
        new_pos = (3 * die) + 6
        die += 3

        positions[player] = (positions[player] + new_pos) % 10
        scores[player] += positions[player] + 1

        player = (player + 1) % len(positions)

    print(min(scores) * die)


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
