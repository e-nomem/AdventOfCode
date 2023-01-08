import asyncio
from itertools import count
from os import path


def simulate_day(octo):
    has_flashed: set[tuple[int, int]] = set()
    for y, row in enumerate(octo):
        for x, val in enumerate(row):
            octo[y][x] += 1

    while True:
        did_flash = False
        for y, row in enumerate(octo):
            for x, val in enumerate(row):
                if val > 9 and (x, y) not in has_flashed:
                    for x_modify in range(max(0, x - 1), min(10, x + 2)):
                        for y_modify in range(max(0, y - 1), min(10, y + 2)):
                            octo[y_modify][x_modify] += 1
                    did_flash = True
                    has_flashed.add((x, y))

        if not did_flash:
            break

    for x, y in has_flashed:
        octo[y][x] = 0

    return len(has_flashed)


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        octo = []
        for line in input_file:
            row = [int(c) for c in line.strip()]
            octo.append(row)

    for day in count(1):
        if simulate_day(octo) == 100:
            print(day)
            break


if __name__ == "__main__":
    asyncio.run(main())
