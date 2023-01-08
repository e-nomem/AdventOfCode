import asyncio
from os import path

from aoclib.timing import benchmark


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    special_cycles = [220, 180, 140, 100, 60, 20]
    cycle = 0
    x_val = 1
    total = 0
    for line in input_lines:
        match line.split():
            case ["addx", val]:
                cycle += 2
                if cycle >= special_cycles[-1]:
                    total += special_cycles[-1] * x_val
                    special_cycles.pop()

                x_val += int(val)
            case ["noop"]:
                cycle += 1
                if cycle >= special_cycles[-1]:
                    total += special_cycles[-1] * x_val
                    special_cycles.pop()

        if not special_cycles:
            break

    print(total)


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l.strip() for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
