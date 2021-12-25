import asyncio
from os import path

from lib.timing import benchmark

CucumberMap = set[tuple[int, ...]]


def move(
    maps: tuple[CucumberMap, ...],
    map_idx: int,
    dimensions: tuple[int, ...],
) -> tuple[tuple[CucumberMap, ...], bool]:
    direction = tuple(1 if d == map_idx else 0 for d in range(len(maps)))
    new_map = set()
    did_update = False
    for point in maps[map_idx]:
        new_point = tuple((a + b) % c for a, b, c in zip(point, direction, dimensions))
        if any(new_point in m for m in maps):
            new_map.add(point)
        else:
            new_map.add(new_point)
            did_update = True

    return maps[:map_idx] + (new_map,) + maps[map_idx + 1 :], did_update


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    east_cucumbers: CucumberMap = set()
    south_cucumbers: CucumberMap = set()

    for y, row in enumerate(input_lines):
        for x, char in enumerate(row):
            if char == ">":
                east_cucumbers.add((x, y))
            elif char == "v":
                south_cucumbers.add((x, y))

    dimensions = (len(input_lines[0]), len(input_lines))
    maps: tuple[CucumberMap, ...] = (east_cucumbers, south_cucumbers)

    for i in range(600):
        updates: list[bool] = []
        for m in range(len(maps)):
            maps, did_update = move(maps, m, dimensions)
            updates.append(did_update)

        if not any(updates):
            print(i)
            break


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l.strip() for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
