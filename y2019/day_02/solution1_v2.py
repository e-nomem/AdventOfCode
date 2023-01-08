import asyncio
from os import path

from ..intcode.executor import run
from ..intcode.utils import load


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        prog = load(input_file.read())
        prog[1] = 12
        prog[2] = 2
        await run(prog)
        print(f"Solution : {prog[0]}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
