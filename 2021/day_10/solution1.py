import asyncio
from os import path
from typing import Optional

CLOSING = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}

POINTS = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}


def score(line: str) -> Optional[int]:
    stack = []
    for char in line:
        if char in CLOSING:
            stack.append(char)
        else:
            open = stack.pop()
            if CLOSING[open] != char:
                return POINTS[char]
    return None


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, 'input.txt')
    with open(infile) as input_file:
        scores = map(score, (l.strip() for l in input_file))
        print(sum(s for s in scores if s is not None))


if __name__ == '__main__':
    asyncio.run(main())
