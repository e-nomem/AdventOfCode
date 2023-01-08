import asyncio
from os import path

from .lib import parse
from aoclib.search import dijkstra
from aoclib.timing import benchmark


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    hallway, starting_rooms = parse(input_lines)
    ending_rooms = tuple(tuple((c,) * len(starting_rooms[0]) for c in "ABCD"))

    starting_state = (hallway, starting_rooms)
    ending_state = (hallway, ending_rooms)

    print(hallway)
    print(starting_rooms)
    # node_map = dijkstra(starting_state, next_steps, lambda n: n == ending_state)
    # print(node_map)


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l.strip() for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
