import asyncio
from os import path

from .lib import Bound
from .lib import build_tree
from .lib import parse
from lib.timing import benchmark


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    target_bound = Bound((-50, -50, -50), (50, 50, 50))
    steps = parse(input_lines, target_bound)
    root = build_tree(steps)

    print(root.cells_active(target_bound))


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
