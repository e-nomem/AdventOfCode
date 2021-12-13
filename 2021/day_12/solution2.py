import asyncio
from collections import Counter
from os import path
from typing import Optional


class Node:
    def __init__(self, name: str) -> None:
        self.name = name
        self.is_small = name.islower()
        self.connected: set[str] = set()

    def add_connection(self, other: 'Node'):
        self.connected.add(other.name)
        other.connected.add(self.name)


def can_visit(next: Node, stack: list[Node]) -> bool:
    if not next.is_small:
        return True

    if next.name == 'start':
        return False

    small_caves = [v.name for v in stack if v.is_small]
    small_caves_set = set(small_caves)
    if next.name not in small_caves_set:
        return True

    return len(small_caves) == len(small_caves_set)


def recurse_find(caves: dict[str, Node], start: Node, end: Node, stack: Optional[list[Node]] = None) -> list[list[Node]]:
    paths: list[list[Node]] = []
    if stack is None:
        stack = []

    if start.name == end.name:
        return [stack[:]]

    stack.append(start)

    for next_name in start.connected:
        next = caves[next_name]
        if can_visit(next, stack):
            paths.extend(recurse_find(caves, next, end, stack))

    stack.pop()
    return paths


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, 'input.txt')
    with open(infile) as input_file:
        caves: dict[str, Node] = {}
        for line in input_file:
            a, b = line.strip().split('-')
            if a in caves:
                node_a = caves[a]
            else:
                node_a = Node(a)
                caves[a] = node_a

            if b in caves:
                node_b = caves[b]
            else:
                node_b = Node(b)
                caves[b] = node_b

            node_a.add_connection(node_b)

        start = caves['start']
        end = caves['end']

        paths = recurse_find(caves, start, end)
        print(len(paths))


if __name__ == '__main__':
    asyncio.run(main())
