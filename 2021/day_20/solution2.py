import asyncio
from functools import reduce
from os import path

from .lib import Algorithm
from .lib import count_lights
from .lib import expand_image
from .lib import Image
from lib.timing import benchmark


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    algorithm: Algorithm = tuple(int(val == "#") for val in input_lines[0].strip())
    image: Image = [[int(val == "#") for val in row.strip()] for row in input_lines[2:]]

    image, _ = reduce(expand_image, range(50), (image, algorithm))

    print(count_lights(image))


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
