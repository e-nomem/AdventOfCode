import asyncio
from os import path

from aoclib.timing import benchmark


def convert_elf_range(inp: str) -> set[int]:
    start, end = (int(x) for x in inp.split("-"))
    return set(range(start, end + 1))


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    sum = 0
    for line in input_lines:
        elf1, elf2 = (convert_elf_range(x) for x in line.split(","))

        if elf1 & elf2:
            sum += 1

    print(sum)


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l.strip() for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
