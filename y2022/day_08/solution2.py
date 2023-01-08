import asyncio
from os import path

from aoclib.timing import benchmark


def visibilityScore(t, r, c):
    left = 0
    top = 0
    right = 0
    bottom = 0
    for i in range(r - 1, -1, -1):
        left += 1
        if t[r][c] <= t[i][c]:
            break
    for i in range(r + 1, len(t)):
        right += 1
        if t[r][c] <= t[i][c]:
            break
    for i in range(c - 1, -1, -1):
        top += 1
        if t[r][c] <= t[r][i]:
            break
    for i in range(c + 1, len(t[r])):
        bottom += 1
        if t[r][c] <= t[r][i]:
            break

    return left * top * bottom * right


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    trees = []
    for line in input_lines:
        trees.append([int(i) for i in line])

    print(
        max(visibilityScore(trees, i, j) for i in range(1, len(trees) - 1) for j in range(1, len(trees[i]) - 1)),
    )


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l.strip() for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
