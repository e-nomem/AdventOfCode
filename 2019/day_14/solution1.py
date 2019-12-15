import asyncio
from collections import Counter
from math import ceil
from os import path
from typing import Dict
from typing import List


CHEMS: Dict['Chemical', List['Chemical']] = {}

CONSUMERS: Dict[str, List[str]] = {}


class Chemical:
    def __init__(self, name: str, amount: int):
        self.name = name
        self.amount = amount

    def __eq__(self, other):
        return self.name == other.name and self.amount == other.amount

    def __hash__(self):
        return hash((self.name, self.amount))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f'{self.name} ({self.amount})'


def process_chem(chem: str) -> Chemical:
    parts = chem.strip().split(maxsplit=1)
    return Chemical(parts[1], int(parts[0]))


def process_input(line: str):
    process = []
    parts = line.split('=>', 1)
    chem_out = process_chem(parts[1])
    for chem_in in parts[0].strip().split(', '):
        c = process_chem(chem_in)
        dep_list = CONSUMERS.get(c.name, [])
        dep_list.append(chem_out.name)
        CONSUMERS[c.name] = dep_list
        process.append(process_chem(chem_in))

    CHEMS[chem_out] = process


def resolve(name: str, current: Counter) -> Counter:
    for c in CHEMS.keys():
        if c.name == name:
            break

    if c.name != name:
        raise RuntimeError(f'Could not find chemical {name}')

    process = CHEMS.get(c)
    if process is None:
        raise RuntimeError(f'Could not find process for {c.name}')

    if current[c.name] >= 0:
        return current

    batches = ceil(abs(current[c.name]) / c.amount)
    for chem in process:
        current[chem.name] -= (chem.amount * batches)

    current[c.name] += (c.amount * batches)
    return current


def make_chemical(name: str = 'FUEL', amount: int = 1) -> int:
    current: Counter = Counter({name: -amount})
    current = resolve(name, current)

    while sum(1 for _, i in current.items() if i < 0) != 1:
        for chem, _ in current.items():
            if chem == 'ORE':
                continue

            if current[chem] >= 0:
                continue

            skip = False
            for consumer in CONSUMERS.get(chem, []):
                if current[consumer] < 0:
                    skip = True
                    break

            if skip:
                continue

            break

        current = resolve(chem, current)

    return abs(current['ORE'])


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, 'input.txt')
    with open(infile, 'r') as input_file:
        for line in input_file:
            process_input(line.strip())

        ore = make_chemical()
        print(f'Solution: {ore}')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
