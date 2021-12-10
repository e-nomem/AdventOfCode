import asyncio
from functools import reduce
from os import path
from statistics import median
from typing import Iterable
from typing import Optional

CLOSING = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}

POINTS = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4,
}


def score(line: str) -> Optional[int]:
    stack = []
    for char in line:
        if char in CLOSING:
            stack.append(char)
        else:
            open = stack.pop()
            if CLOSING[open] != char:
                return None

    return reduce(lambda acc, c: (acc * 5) + POINTS[c], reversed(stack), 0)


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, 'input.txt')
    with open(infile) as input_file:
        scores = map(score, (l.strip() for l in input_file))
        print(median(s for s in scores if s is not None))



if __name__ == '__main__':
    asyncio.run(main())
