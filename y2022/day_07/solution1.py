import asyncio
from collections import defaultdict
from os import path

from aoclib.timing import benchmark


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    cur_path = "/"
    dirs = defaultdict(int)
    for line in input_lines:
        match line.split():
            case ["$", "cd", p]:
                cur_path = path.abspath(path.join(cur_path, p))
            case ["$", "ls"]:
                continue
            case ["dir", _]:
                continue
            case [size, file]:
                local_path = path.join(cur_path, file)
                val = int(size)
                head, _ = path.split(local_path)
                while True:
                    dirs[head] += val
                    if head == "/":
                        break
                    head, _ = path.split(head)

    print(sum(v for v in dirs.values() if v <= 100000))


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l.strip() for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
