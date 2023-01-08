import asyncio
from os import path

from aoclib.timing import benchmark


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    elves = []
    elf = []
    for line in input_lines:
        if line:
            elf.append(int(line))
        else:
            elves.append(elf)
            elf = []

    elves.append(elf)

    print(max(sum(e) for e in elves))


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l.strip() for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
