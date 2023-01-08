import asyncio
from os import path

from aoclib.timing import benchmark

SCREEN_WIDTH = 40


def print_pixel(cycle: int, x_pos: int):
    cursor = cycle % SCREEN_WIDTH

    if cursor == 0:
        print()

    char = " "
    if cursor in set(range(x_pos - 1, x_pos + 2)):
        char = "█"

    print(char, end="")


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    cycle = 0
    x_val = 1
    for line in input_lines:
        match line.split():
            case ["addx", val]:
                for _ in range(2):
                    print_pixel(cycle, x_val)
                    cycle += 1

                x_val += int(val)
            case ["noop"]:
                print_pixel(cycle, x_val)
                cycle += 1


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l.strip() for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
