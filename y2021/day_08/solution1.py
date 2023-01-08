import asyncio
from os import path


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        count = 0
        for line in input_file:
            results = line.strip().split(" | ", 1)[1].split(" ")
            for r in results:
                if len(r) in {2, 3, 4, 7}:
                    count += 1

        print(count)


if __name__ == "__main__":
    asyncio.run(main())
