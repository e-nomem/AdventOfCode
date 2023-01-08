import asyncio
from os import path

from aoclib.timing import benchmark


def visible(trees: list[list[int]], row: int, col: int) -> bool:
    if row == 0 or col == 0 or row == len(trees) - 1 or col == len(trees[row]) - 1:
        return True
    for i in range(1, row + 1):
        if trees[row][col] <= trees[row - i][col]:
            break
        if row == i:
            return True
    for i in range(row + 1, len(trees)):
        if trees[row][col] <= trees[i][col]:
            break
        if i == len(trees) - 1:
            return True
    for i in range(1, col + 1):
        if trees[row][col] <= trees[row][col - i]:
            break
        if col == i:
            return True
    for i in range(col + 1, len(trees[row])):
        if trees[row][col] <= trees[row][i]:
            break
        if i == len(trees[row]) - 1:
            return True
    return False


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    trees = []
    for line in input_lines:
        trees.append([int(i) for i in line])

    print(
        sum(1 for i in range(len(trees)) for j in range(len(trees[i])) if visible(trees, i, j)),
    )


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l.strip() for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
