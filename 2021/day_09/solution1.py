import asyncio
from os import path


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, 'input.txt')
    with open(infile) as input_file:
        map = []
        for line in input_file:
            map.append([int(i) for i in line.strip()])

        sum = 0

        for y, row in enumerate(map):
            for x, val in enumerate(row):
                if x != 0 and map[y][x-1] <= val:
                    continue
                if x != len(row) - 1 and map[y][x+1] <= val:
                    continue
                if y != 0 and map[y-1][x] <= val:
                    continue
                if y != len(map) - 1 and map[y+1][x] <= val:
                    continue

                sum += val + 1

        print(sum)


if __name__ == '__main__':
    asyncio.run(main())
