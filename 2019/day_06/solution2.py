from os import path
from typing import Dict
from typing import List
from typing import Optional


class Orbit:
    def __init__(self, name: str, parent: Optional['Orbit'] = None) -> None:
        self.name = name
        self.parent = parent

    def ancestors(self) -> List['Orbit']:
        ancestors: List['Orbit'] = []
        node = self.parent
        while node is not None:
            ancestors.insert(0, node)
            node = node.parent

        return ancestors

    def common_ancestor(self, other: 'Orbit') -> Optional['Orbit']:
        my_ancestors = self.ancestors()
        other_ancestors = other.ancestors()
        for i in range(len(my_ancestors)):
            if my_ancestors[i].name != other_ancestors[i].name:
                return my_ancestors[i - 1]
        return None

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

        santa = orbit_map.get('SAN')
        you = orbit_map.get('YOU')

        if not santa:
            raise RuntimeError('Unable to find SAN in input')

        if not you:
            raise RuntimeError('Unable to find YOU in input')

        ancestor = santa.common_ancestor(you)
        if not ancestor:
            raise RuntimeError('Unable to find a common ancestor between SAN and YOU')

        distance = you.distance(ancestor.name) + santa.distance(ancestor.name) - 2
        print(f'Distance to Santa: {distance}')


if __name__ == '__main__':
    main()
