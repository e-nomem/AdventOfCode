from collections.abc import Callable
from collections.abc import Iterable
from collections.abc import Iterator
from collections.abc import Sequence
from typing import TypeVar

_State = TypeVar("_State")


class Node:
    def __init__(self, name: str) -> None:
        self.name = name
        self.is_small = name.islower()
        self.connected: set[str] = set()

    def add_connection(self, other: "Node"):
        self.connected.add(other.name)
        other.connected.add(self.name)

    def __repr__(self) -> str:
        return f"Node<{self.name}>"


def neighbors(
    caves: dict[str, Node],
    can_visit: Callable[[Node, Sequence[Node], _State], tuple[bool, _State]],
) -> Callable[[Sequence[Node], _State], Iterable[tuple[Node, _State]]]:
    def _helper(path: Sequence[Node], state: _State) -> Iterator[tuple[Node, _State]]:
        for next_name in path[-1].connected:
            next_node = caves[next_name]
            allowed, next_state = can_visit(next_node, path, state)
            if allowed:
                yield next_node, next_state

    return _helper


def parse_caves(input_lines: list[str]) -> dict[str, Node]:
    caves: dict[str, Node] = {}
    for line in input_lines:
        a, b = line.split("-")
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

    return caves
