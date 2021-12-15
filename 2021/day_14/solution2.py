import asyncio
from collections import Counter
from functools import reduce
from os import path

from ..day_01.lib import window


def step(polymers: Counter[tuple[str, str]], patterns: dict[tuple[str, str], str]) -> Counter[tuple[str, str]]:
    next_polymer: Counter[tuple[str, str]] = Counter()
    for polymer, count in polymers.items():
        insert = patterns[polymer]
        next_polymer[(polymer[0], insert)] += count
        next_polymer[(insert, polymer[1])] += count

    return next_polymer


def calculate(polymers: Counter[tuple[str, str]], template: str) -> int:
    c: Counter[str] = Counter(template[-1])

    for polymer, count in polymers.items():
        c[polymer[0]] += count

    min_count = min(c.values())
    max_count = max(c.values())

    return max_count - min_count


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, 'input.txt')
    with open(infile) as input_file:
        patterns: dict[tuple[str, str], str] = {}
        template = next(input_file).strip()
        polymers: Counter[tuple[str, str]] = Counter(window(template))
        next(input_file)

        for line in input_file:
            pattern, insert = line.strip().split(' -> ')
            patterns[(pattern[0], pattern[1])] = insert

    final = reduce(lambda acc, _step: step(acc, patterns), range(40), polymers)

    print(calculate(final, template))


if __name__ == '__main__':
    asyncio.run(main())
