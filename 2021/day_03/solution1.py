import asyncio
from collections import Counter
from os import path


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, 'input.txt')
    with open(infile) as input_file:
        c: Counter[int] = Counter()
        for line in input_file:
            for idx, char in enumerate(line.strip()):
                mod = 1 if int(char) else -1
                c[idx] += mod

        gamma = 0
        epsilon = 0
        for idx, val in c.items():
            if val > 0:
                gamma = (gamma << 1) + 1
                epsilon = epsilon << 1
            else:
                gamma = gamma << 1
                epsilon = (epsilon << 1) + 1

        print(gamma * epsilon)


if __name__ == '__main__':
    asyncio.run(main())
