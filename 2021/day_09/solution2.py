import asyncio
from functools import reduce
from heapq import heappush
from heapq import heappushpop
from os import path

Point = tuple[int, int]


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        map = []
        for line in input_file:
            map.append([int(i) for i in line.strip()])

        # Map from point to the associated basin origin
        belonging: dict[Point, Point] = {}

        # Map from a basin origin to all points in that basin
        basins: dict[Point, set[Point]] = {}

        for y, row in enumerate(map):
            for x, val in enumerate(row):
                if val == 9:
                    continue

                belong_x = None
                belong_y = None
                if x != 0 and map[y][x - 1] != 9:
                    belong_x = belonging[(x - 1, y)]
                    belonging[(x, y)] = belong_x
                    basins[belong_x].add((x, y))

                if y != 0 and map[y - 1][x] != 9:
                    belong_y = belonging[(x, y - 1)]
                    belonging[(x, y)] = belong_y
                    basins[belong_y].add((x, y))

                if belong_x is None and belong_y is None:
                    # This is now the origin of a new basin
                    belonging[(x, y)] = (x, y)
                    basins[(x, y)] = {(x, y)}
                elif belong_x is not None and belong_y is not None and belong_x != belong_y:
                    # Two separate basins are connected at this point
                    # Merge the two of them together
                    for point in basins[belong_x]:
                        belonging[point] = belong_y
                        basins[belong_y].add(point)

                    del basins[belong_x]

        heap: list[int] = []
        for points in basins.values():
            if len(heap) < 3:
                heappush(heap, len(points))
            else:
                heappushpop(heap, len(points))

        print(reduce(lambda acc, i: acc * i, heap, 1))


if __name__ == "__main__":
    asyncio.run(main())
