import asyncio
from functools import reduce
from os import path

from .lib2 import make_value_generators
from aoclib.timing import benchmark

# Through some analysis, we can figure out the following about the algorithm.
# The code, as provided, does the following:
#
# x = (z % 26) + X_ADD != INPUT
# z //= DIVIDE <-- It should be noted that his is only ever 1 or 26. This is important
# z *= 26 if x else 1
# z += INPUT + Y_ADD if x else 0
#
# Or written another way,
# x = (z % 26) + X_ADD != INPUT
# z //= DIVIDE
# if x:
#     z = (z * 26) + INPUT + Y_ADD
#
# These multiplication, division, and modulus operations are basically shifting digits
# in and out of a base 26 number. This is easier to visualize if you use base 10 instead.
# Also, the value of DIVIDE and X_ADD are linked such that x is always true if DIVIDE is 1.
# The pseudocode then becomes:
# x = (z % 26) + X_ADD != INPUT
# if x:
#     push(z, INPUT + Y_ADD)
# else:
#     pop(z)
#     if x:
#         push(z, INPUT + Y_ADD)
#
# To get a final 0 value for z, our z stack needs to be empty. Each block of operations then
# results in one of the following operations, PUSH, POP/PUSH, POP. To end up with an empty stack,
# we need to block the POP/PUSH operation by ensuring that x is false.
#
# Working through the provided puzzle input, we eventually obtain the constraints:
# input[3] = input[2] + 6
# input[4] = input[1] + 5
# input[6] = input[5] + 1
# input[7] = input[0] + -1
# input[9] = input[8] + -5
# input[12] = input[11] + -4
# input[13] = input[10] + 0
#
# We can now use these to generate all possible valid inputs


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    program = tuple(tuple(l.split()) for l in input_lines)
    value_generators = make_value_generators(program)

    values: tuple[int, ...] = ()
    values = reduce(lambda vals, gen: vals + (max(gen(vals)),), value_generators, values)
    print(reduce(lambda acc, n: (acc * 10) + n, values))


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l.strip() for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
