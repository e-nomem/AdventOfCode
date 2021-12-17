import asyncio
import decimal
from collections.abc import Callable
from decimal import Decimal
from os import path
from statistics import mean


def distance_from(pos: Decimal) -> Callable[[Decimal], Decimal]:
    def _helper(crab: Decimal) -> Decimal:
        return abs(pos - crab)

    return _helper


def triangle(i: Decimal) -> Decimal:
    return (i ** 2 + i) // 2


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        crabs = [Decimal(p) for p in next(input_file).strip().split(",")]
        mean_pos = mean(crabs).quantize(1, decimal.ROUND_05UP)

        print(sum(map(triangle, map(distance_from(mean_pos), crabs))))


if __name__ == "__main__":
    asyncio.run(main())
