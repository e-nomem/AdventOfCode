import asyncio
from os import path

from ..intcode.executor import run
from ..intcode.io import static
from ..intcode.utils import load


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        prog = load(input_file.read())
        reader = static(5)
        await run(prog, reader=reader)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
