import asyncio
from os import path

from ..intcode.executor import run
from ..intcode.utils import load
from ..util import Point


def prog_logic():
    scaffold = {}
    x = 0
    y = 0

    async def _writer(val: int) -> None:
        nonlocal x
        nonlocal y
        c = chr(val)
        if c == "#":
            scaffold.add(Point(x, y))

        if c == "\n":
            x = 0
            y += 1
        else:
            x += 1


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        prog = load(input_file.read())
        await run(prog, writer=print_char)
        print()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
