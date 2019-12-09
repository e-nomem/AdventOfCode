import asyncio
from itertools import permutations
from os import path

from ..intcode.executor import run_program
from ..intcode.io import pipe
from ..intcode.io import spread_write
from ..intcode.utils import load_program_from_string
from ..intcode.utils import Program


async def run_amplifiers_feedback(prog: Program, count: int = 5) -> int:
    phase_settings = list(permutations(range(count, count * 2)))  # Phase range for feedback is higher
    values = []

    for setting in phase_settings:
        last_output = 0

        async def save_output(val: int) -> None:
            nonlocal last_output
            last_output = val

        pipes = [pipe(setting[0], 0)]  # First pipe has an extra input of '0' as the initial value
        for i in range(1, count):
            pipes.append(pipe(setting[i]))

        programs = []  # List of programs running in parallel
        for i in range(count):
            # Reader comes from pipes[i]
            # Writer comes from pipes[i+1]
            reader, _ = pipes[i]
            if i + 1 == len(pipes):
                _, writer = pipes[0]  # Loop back around
                writer = spread_write(writer, save_output)  # Send output to next amp and save it for later
            else:
                _, writer = pipes[i + 1]

            programs.append(run_program(prog.copy(), reader=reader, writer=writer))

        await asyncio.wait(programs)  # Wait for all programs to terminate
        values.append(last_output)

    # Now that all the amplifiers have run, return the max output
    return max(values)


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, 'input.txt')
    with open(infile, 'r') as input_file:
        prog = load_program_from_string(input_file.read())
        max_output = await run_amplifiers_feedback(prog)
        print(f'Maximum Output: {max_output}')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
