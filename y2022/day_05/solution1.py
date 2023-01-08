import asyncio
from os import path

from aoclib.timing import benchmark


def init_stacks(lines):
    stacks = [[] for _ in range((len(lines[0]) + 1) // 4)]
    for lineno, line in enumerate(lines):
        if not line:
            break

        for idx in range(len(stacks)):
            char = line[(idx * 4) + 1]
            if char.strip():
                stacks[idx].append(char)

    for stack in stacks:
        stack.pop()
        stack.reverse()

    return stacks, lines[lineno + 1 :]


def parse_line(line: str):
    _, count, _, source, _, dest = line.split(" ")
    return int(count), int(source) - 1, int(dest) - 1


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    stacks, input_lines = init_stacks(input_lines)

    for line in input_lines:
        count, source, dest = parse_line(line)
        stacks[dest].extend(reversed(stacks[source][-count:]))
        del stacks[source][-count:]

    for stack in stacks:
        print(stack[-1], end="")

    print()


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l[:-1] if l[-1] == "\n" else l for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
