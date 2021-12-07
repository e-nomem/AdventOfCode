import asyncio
import decimal
from decimal import Decimal
from os import path
from statistics import mean


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, 'input.txt')
    with open(infile) as input_file:
        crabs = [Decimal(p) for p in next(input_file).strip().split(',')]
        mean_pos = mean(crabs).quantize(1, decimal.ROUND_05UP)
        fuel = sum(((d ** 2) + d) // 2 for c in crabs for d in [abs(mean_pos - c)])
        print(fuel)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
