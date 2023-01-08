import asyncio
from collections import Counter
from os import path


def fuel_req(pos, crabs):
    fuel = 0
    for key, val in crabs.items():
        dist = abs(pos - key)
        fuel += dist * val

    return fuel


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        crabs = Counter(int(p) for p in next(input_file).strip().split(","))
        min_pos = min(crabs.keys())
        max_pos = max(crabs.keys())

        print(min(fuel_req(pos, crabs) for pos in range(min_pos, max_pos + 1)))


if __name__ == "__main__":
    asyncio.run(main())
