import asyncio
from os import path

from ..intcode.executor import run
from ..intcode.utils import load
from ..intcode.utils import Program


async def find_inputs(prog: Program, solution: int = 19690720) -> int:
    for noun in range(100):
        for verb in range(100):
            p = prog.copy()
            p[1] = noun
            p[2] = verb
            await run(p)
            if p[0] == solution:
                return (100 * noun) + verb
    return -1


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, 'input.txt')
    with open(infile, 'r') as input_file:
        prog = load(input_file.read())
        output = await find_inputs(prog)
        print(f'Solution : {output}')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
