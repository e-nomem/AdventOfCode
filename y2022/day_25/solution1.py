import asyncio
from itertools import zip_longest
from os import path

from aoclib.timing import benchmark


def format_balanced_base_five(n: list[int]) -> str:
    chars = ""
    for i in n:
        match i:
            case -2:
                chars += "="
            case -1:
                chars += "-"
            case val:
                chars += str(val)

    return chars


def parse_balanced_base_five(n: str) -> list[int]:
    digits = []
    for c in n:
        match c:
            case "=":
                digits.append(-2)
            case "-":
                digits.append(-1)
            case val:
                digits.append(int(val))

    return digits


def add_balanced(base: int, *numbers: list[int]) -> list[int]:
    if not base % 2:
        raise Exception("Only odd bases can be balanced")

    shift = base // 2
    total = []
    carry = 0
    for n in zip_longest(*(reversed(nums) for nums in numbers), fillvalue=0):
        digit = sum(n) + carry + shift
        carry = digit // base
        total.append((digit % base) - shift)

    if carry:
        total.append(carry)

    return total[::-1]


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    numbers = [parse_balanced_base_five(l) for l in input_lines]
    total = add_balanced(5, *numbers)

    print(format_balanced_base_five(total))


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l.strip() for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
