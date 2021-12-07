import asyncio
from os import path
from statistics import median


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, 'input.txt')
    with open(infile) as input_file:
        crabs = [int(p) for p in next(input_file).strip().split(',')]
        median_pos = int(median(crabs))

        print(sum(abs(median_pos - i) for i in crabs))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
