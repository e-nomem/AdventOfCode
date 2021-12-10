import asyncio
from functools import reduce
from os import path
from typing import Iterable


CANONICAL = {
    frozenset('abcefg'): 0,
    frozenset('cf'): 1,
    frozenset('acdeg'): 2,
    frozenset('acdfg'): 3,
    frozenset('bcdf'): 4,
    frozenset('abdfg'): 5,
    frozenset('abdefg'): 6,
    frozenset('acf'): 7,
    frozenset('abcdefg'): 8,
    frozenset('abcdfg'): 9,
}


def decode(inputs: Iterable[str]) -> dict[str, str]:
    mapping = {}
    sets = [set(e) for e in inputs]

    # Unique values 1, 4, 7
    one = [i for i in sets if len(i) == 2][0]
    four = [i for i in sets if len(i) == 4][0]
    seven = [i for i in sets if len(i) == 3][0]

    # Non-unique values
    twothreefive = [i for i in sets if len(i) == 5]

    adg = reduce(lambda acc, i: acc & i, twothreefive)

    a = list(adg & seven)[0]
    mapping[a] = 'a'

    d = list(adg & four)[0]
    mapping[d] = 'd'

    g = list(adg - {a, d})[0]
    mapping[g] = 'g'

    two = [i for i in twothreefive if len(i & four) == 2][0]

    c = list(two & one)[0]
    mapping[c] = 'c'

    f = list(one - {c})[0]
    mapping[f] = 'f'

    b = list(four - {c, d, f})[0]
    mapping[b] = 'b'

    e = list(two - {a, c, d, g})[0]
    mapping[e] = 'e'

    return mapping


def process(inputs: Iterable[str], outputs: Iterable[str]) -> int:
    mapped_segments = decode(inputs)
    val = 0
    for output in outputs:
        canonical = frozenset(mapped_segments[c] for c in output)
        val *= 10
        val += CANONICAL[canonical]

    return val


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, 'input.txt')
    total = 0
    with open(infile) as input_file:
        for line in input_file:
            inputs, outputs = (r.split(' ') for r in line.strip().split(' | ', 1))
            total += process(inputs, outputs)

        print(total)


if __name__ == '__main__':
    asyncio.run(main())
