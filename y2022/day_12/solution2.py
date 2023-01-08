import asyncio
from collections import deque
from os import path

from aoclib.timing import benchmark

DIRECTIONS = (
    (1, 0),
    (0, 1),
    (0, -1),
    (-1, 0),
)


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    start = None
    end = None
    elevations = {}

    for y, line in enumerate(input_lines):
        for x, char in enumerate(line):
            if char == "S":
                start = (x, y)
                char = "a"
            elif char == "E":
                end = (x, y)
                char = "z"

            elevations[(x, y)] = ord(char) - ord("a")

    cost_map = {
        end: 0,
    }
    queue = deque([end])
    while queue:
        cur_loc = queue.popleft()
        cur_elev = elevations[cur_loc]
        cur_cost = cost_map[cur_loc]
        for dir in DIRECTIONS:
            new_loc = tuple(map(sum, zip(cur_loc, dir)))
            if new_loc in elevations and new_loc not in cost_map:
                new_elev = elevations[new_loc]
                if new_elev >= cur_elev - 1:
                    cost_map[new_loc] = cur_cost + 1
                    if new_elev == 0:
                        print(cost_map[new_loc])
                        return

                    queue.append(new_loc)


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l.strip() for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
