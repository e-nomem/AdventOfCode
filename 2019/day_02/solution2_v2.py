import asyncio
from os import path
from typing import List

from ..intcode.executor import run_program
from ..intcode.utils import load_program_from_string


async def find_inputs(prog: List[int], solution: int = 19690720) -> int:
    for noun in range(100):
        for verb in range(100):
            p = prog.copy()
            p[1] = noun
            p[2] = verb
            await run_program(p)
            if p[0] == solution:
                return (100 * noun) + verb
    return -1


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, 'input.txt')
    with open(infile, 'r') as input_file:
        prog = load_program_from_string(input_file.read())
        output = await find_inputs(prog)
        print(f'Solution : {output}')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
