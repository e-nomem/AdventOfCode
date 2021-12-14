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
    c: Counter[str] = Counter()

    # This loop will double count every character except for the first and last one
    for polymer, count in polymers.items():
        c[polymer[0]] += count
        c[polymer[1]] += count

    # Adjust for the under counting of the first and last chars here
    c[template[0]] += 1
    c[template[-1]] += 1

    min_count = min(c.values())
    max_count = max(c.values())

    # Since we double count everything, divide by two
    return (max_count - min_count) // 2


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
