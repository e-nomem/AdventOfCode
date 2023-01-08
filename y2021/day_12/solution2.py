import asyncio
from collections.abc import Sequence
from os import path
from typing import Optional

from .lib import neighbors
from .lib import Node
from .lib import parse_caves
from aoclib.search import dfs
from aoclib.timing import benchmark


def can_visit(next: Node, stack: Sequence[Node], state: Optional[str]) -> tuple[bool, Optional[str]]:
    if not next.is_small:
        return True, state

    if next.name == "start":
        return False, state

    if next.name in {v.name for v in stack if v.is_small}:
        return state is None, state or next.name

    return True, state


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    caves = parse_caves(input_lines)

    start = caves["start"]
    end = caves["end"]

    paths = dfs(start, neighbors(caves, can_visit), lambda n, _: n.name == end.name)
    print(len(paths))


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l.strip() for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
