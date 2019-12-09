from os import path
from typing import Dict
from typing import Optional


class Orbit:
    def __init__(self, name: str, parent: Optional['Orbit'] = None) -> None:
        self.name = name
        self.parent = parent

    def distance(self, loc: str = 'COM') -> int:
        node: Optional['Orbit'] = self
        depth = 0
        while node is not None and node.name != loc:
            depth += 1
            node = node.parent
        return depth


def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, 'input.txt')
    with open(infile, 'r') as input_file:
        orbit_map: Dict[str, Orbit] = {}
        for line in input_file:
            parts = line.strip().split(')', 1)
            parent = orbit_map.get(parts[0])
            if parent is None:
                parent = Orbit(parts[0])
                orbit_map[parent.name] = parent

            child = orbit_map.get(parts[1])
            if child is None:
                child = Orbit(parts[1], parent)
                orbit_map[child.name] = child
            else:
                child.parent = parent

        orbits = sum(o.distance() for _, o in orbit_map.items())
        print(f'Number of Orbits: {orbits}')


if __name__ == '__main__':
    main()
