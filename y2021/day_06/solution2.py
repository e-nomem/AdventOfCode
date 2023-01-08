import asyncio
from collections import Counter
from functools import reduce
from os import path


def simulate_day(fish: Counter[int]) -> Counter[int]:
    new_fish = Counter({f - 1: num for f, num in fish.items()})
    respawns = new_fish[-1]
    new_fish[6] += respawns
    new_fish[8] += respawns
    del new_fish[-1]

    return new_fish


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        line = next(line.strip() for line in input_file)

        fish = Counter(int(i) for i in line.split(","))
        fish = reduce(lambda acc, _: simulate_day(acc), range(256), fish)

        print(sum(fish.values()))


if __name__ == "__main__":
    asyncio.run(main())
