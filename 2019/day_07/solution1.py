import asyncio
from itertools import permutations
from os import path

from ..intcode.executor import run_program
from ..intcode.io import pipe
from ..intcode.utils import load_program_from_string
from ..intcode.utils import Program


async def run_amplifiers(prog: Program, count: int = 5) -> int:
    phase_settings = list(permutations(range(count)))
    values = []

    async def accumulator(val: int) -> None:
        values.append(val)

    for setting in phase_settings:
        pipes = [pipe(setting[0], 0)]  # First pipe has an extra input of '0' as the initial value
        for i in range(1, count):
            pipes.append(pipe(setting[i]))

        for i in range(count):
            # Reader comes from pipes[i]
            # Writer comes from pipes[i+1]
            reader, _ = pipes[i]
            if i + 1 == len(pipes):
                writer = accumulator  # Special case, final value is collected
            else:
                _, writer = pipes[i + 1]

            await run_program(prog.copy(), reader=reader, writer=writer)

    # Now that all the amplifiers have run, return the max output
    return max(values)


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, 'input.txt')
    with open(infile, 'r') as input_file:
        prog = load_program_from_string(input_file.read())
        max_output = await run_amplifiers(prog)
        print(f'Maximum Output: {max_output}')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
