import asyncio
from collections.abc import Callable
from operator import add
from operator import mul
from os import path

from aoclib.itertools import chunked
from aoclib.itertools import take
from aoclib.timing import benchmark


class Monkey:
    def __init__(
        self,
        items: list[int],
        op: Callable[[int], int],
        test: Callable[[int], int],
    ) -> None:
        self.items = items
        self.op = op
        self.test = test
        self.inspections = 0

    def execute_turn(self) -> dict[int, list[int]]:
        destination = {}
        self.inspections += len(self.items)
        for item in self.items:
            item = self.op(item)
            item //= 3
            dest = self.test(item)
            if dest not in destination:
                destination[dest] = []

            destination[dest].append(item)

        self.items = []
        return destination


def parse_monkey(config: list[str]) -> Monkey:
    starting_items = [int(i) for i in config[1].split(":")[1].strip().split(", ")]
    k1, op_sym, k2 = config[2][19:].split()
    match op_sym:
        case "+":
            operator = add
        case "*":
            operator = mul

    if k1 != "old":
        raise Exception("Cannot deal with this")

    if k2 != "old":
        op = lambda i: operator(i, int(k2))
    else:
        op = lambda i: operator(i, i)

    test_val = int(config[3][21:])
    true_dest = int(config[4][29:])
    false_dest = int(config[5][30:])
    test = lambda i: true_dest if (i % test_val) == 0 else false_dest

    return Monkey(starting_items, op, test)


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    monkeys = [parse_monkey(config) for config in chunked(7, input_lines)]

    for round in range(20):
        for idx, monkey in enumerate(monkeys):
            throws = monkey.execute_turn()
            for dest, items in throws.items():
                monkeys[dest].items.extend(items)

    m1, m2 = take(2, sorted(monkeys, key=lambda m: m.inspections, reverse=True))
    print(m1.inspections * m2.inspections)


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l.rstrip() for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
