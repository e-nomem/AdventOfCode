import asyncio
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


def resolve(name: str, amount: int, have: Dict[str, int]) -> Dict[str, int]:
    needed: Dict[str, int] = {}
    for c in CHEMS.keys():
        if c.name == name:
            break

    if c.name != name:
        return needed

    overflow_amount = have.get(c.name, 0)
    if overflow_amount >= amount:
        overflow_amount -= amount
        have[c.name] = overflow_amount
        return needed
    else:
        have[c.name] = 0

    amount -= overflow_amount
    count = ceil(amount / c.amount)
    process = CHEMS.get(c)
    if process is None:
        raise RuntimeError(f'Could not find process for {c.name}')

    for chem in process:
        a = needed.get(chem.name, 0)
        needed[chem.name] = a + (chem.amount * count)

    overflow_amount = (c.amount * count) - amount
    have[c.name] = overflow_amount
    return needed


def make_chemical(name: str = 'FUEL', amount: int = 1) -> int:
    needed: Dict[str, int] = {}
    have: Dict[str, int] = {}
    for current_chem in CHEMS.keys():
        if current_chem.name == name:
            break

    needed.update(resolve(current_chem.name, amount, have))

    while len(needed) != 1:
        for chem, _ in needed.items():
            if chem == 'ORE':
                continue

            skip = False
            for consumer in CONSUMERS.get(chem, []):
                if needed.get(consumer, 0) != 0:
                    skip = True
                    break

            if skip:
                continue

            break

        amt = needed.pop(chem, 0)
        for c, a in resolve(chem, amt, have).items():
            current = needed.get(c, 0)
            needed[c] = current + a

    return needed.get('ORE', -1)


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
