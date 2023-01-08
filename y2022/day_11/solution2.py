import asyncio
from collections.abc import Callable
from functools import reduce
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
        test: int,
        true_dest: int,
        false_dest: int,
    ) -> None:
        self.items = items
        self.op = op
        self.test = test
        self.true_dest = true_dest
        self.false_dest = false_dest
        self.inspections = 0

    def __repr__(self) -> str:
        return f"Monkey<items={len(self.items)}, test={self.test}, true={self.true_dest}, false={self.false_dest}, inspections={self.inspections}>"

    def execute_turn(self) -> dict[int, list[int]]:
        destination = {}
        self.inspections += len(self.items)
        for item in self.items:
            item = self.op(item)
            dest = self.false_dest if item % self.test else self.true_dest
            if dest not in destination:
                destination[dest] = []

            destination[dest].append(item)

        del self.items[:]
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

    test = int(config[3][21:])
    true_dest = int(config[4][29:])
    false_dest = int(config[5][30:])

    return Monkey(starting_items, op, test, true_dest, false_dest)


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    monkeys = [parse_monkey(config) for config in chunked(7, input_lines)]

    supermod = reduce(mul, (m.test for m in monkeys), 1)

    for _ in range(10000):
        for monkey in monkeys:
            throws = monkey.execute_turn()
            for dest, items in throws.items():
                monkeys[dest].items.extend(i % supermod for i in items)

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
