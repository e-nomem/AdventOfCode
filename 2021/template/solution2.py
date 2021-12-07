import asyncio
from os import path


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, 'input.txt')
    with open(infile) as input_file:  # noqa: F841
        pass


if __name__ == '__main__':
    asyncio.run(main())
