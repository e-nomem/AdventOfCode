from functools import reduce
from itertools import chain
from operator import add
from operator import mul
from typing import cast
from typing import Optional
from typing import Union

Point = tuple[int, ...]


class Bound:
    def __init__(self, min: Point, max: Point) -> None:
        self.min = min
        self.max = max

    def union(self, other: "Bound") -> "Bound":
        new_min = tuple(min(d) for d in zip(self.min, other.min))
        new_max = tuple(max(d) for d in zip(self.max, other.max))
        return Bound(new_min, new_max)

    def intersection(self, other: "Bound") -> "Bound":
        new_min = tuple(max(d) for d in zip(self.min, other.min))
        new_max = tuple(min(d) for d in zip(self.max, other.max))
        return Bound(new_min, new_max)

    def overlaps(self, other: "Bound") -> bool:
        return all(a <= b for a, b in chain(zip(self.min, other.max), zip(other.min, self.max)))

    def contains(self, other: "Bound") -> bool:
        return all(a <= b for a, b in chain(zip(self.min, other.min), zip(other.max, self.max)))

    def volume(self) -> int:
        return reduce(mul, (max - min + 1 for max, min in zip(self.max, self.min)))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}<{self.min}, {self.max}>"


class DimensionTreeNode:
    def __init__(self, on: bool, bound: Bound) -> None:
        # This state var has an odd type but it represents the two possible states of this node:
        #   1. This node represents a contigious region, and stores the on/off bool as the state
        #   2. This node represents a partitioned region, and stores the children as the state
        self.state: Union[bool, tuple[DimensionTreeNode, DimensionTreeNode]] = on
        self.bound = bound

    def partition(self, on: bool, bound: Bound) -> None:
        if not self.bound.overlaps(bound):
            return

        if bound.contains(self.bound):
            # Our region is entirely overwritten
            self.state = on
            return

        if isinstance(self.state, tuple):
            # Pass the new state info to the children
            for child in self.state:
                child.partition(on, bound)

            if self._can_collapse_children():
                # Both children are leaves and have the same internal state, merge them back into this node
                self.state = self.state[0].state

            return

        if self.state == on:
            # Current state and intended state are the same, nothing to do
            return

        # The new bound partially overlaps our own bound
        # Need to partition our space by creating children
        # At any given node, we only split on a single plane/axis
        for axis in range(len(self.bound.min)):
            if self.bound.min[axis] < bound.min[axis]:
                partition_point = bound.min[axis] - 1
            elif bound.max[axis] < self.bound.max[axis]:
                partition_point = bound.max[axis]
            else:
                continue

            # We found a candidate axis on which to partition, so create the children
            left_bound = Bound(
                self.bound.min,
                (self.bound.max[:axis] + (partition_point,) + self.bound.max[axis + 1 :]),
            )
            left_child = DimensionTreeNode(self.state, left_bound)
            right_bound = Bound(
                (self.bound.min[:axis] + (partition_point + 1,) + self.bound.min[axis + 1 :]),
                self.bound.max,
            )
            right_child = DimensionTreeNode(self.state, right_bound)
            self.state = (left_child, right_child)
            break

        # Now that the children have been created, recursively call partition on them
        # since we may need to partition on multiple axes for a single bound or update their internal state
        assert isinstance(self.state, tuple)
        for child in self.state:
            child.partition(on, bound)

    def cells_active(self, bound: Optional[Bound] = None) -> int:
        if bound is None:
            bound = self.bound

        if not self.bound.overlaps(bound):
            return 0

        if isinstance(self.state, tuple):
            return reduce(add, (c.cells_active(bound) for c in self.state))

        if self.state:
            return self.bound.intersection(bound).volume()

        return 0

    def is_active(self, point: Point) -> bool:
        bound = Bound(point, point)
        return self.cells_active(bound) == 1

    def _can_collapse_children(self) -> bool:
        assert isinstance(self.state, tuple)
        it = (c.state if isinstance(c.state, bool) else None for c in self.state)
        return cast(bool, reduce(lambda acc, b: acc is not None and acc == b, it))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}<state={self.state if isinstance(self.state, bool) else 'partitioned'}, bound={self.bound}>"


def parse(lines: list[str], target: Optional[Bound] = None) -> list[tuple[bool, Bound]]:
    steps: list[tuple[bool, Bound]] = []
    for line in lines:
        action, bound_str = line.strip().split(" ", 1)
        min_vals = []
        max_vals = []
        for dimension in bound_str.split(","):
            bounds = dimension.split("=")[1]
            min_dimension, max_dimension = map(int, bounds.split(".."))
            min_vals.append(min_dimension)
            max_vals.append(max_dimension)

        bound = Bound(tuple(min_vals), tuple(max_vals))
        if target is None:
            steps.append((action == "on", bound))
        elif bound.overlaps(target):
            steps.append((action == "on", bound.intersection(target)))

    return steps


def build_tree(steps: list[tuple[bool, Bound]]) -> DimensionTreeNode:
    # Build the widest possible bound for all the given inputs to use at the root
    max_bound = reduce(lambda acc, bound: acc.union(bound), (b for _, b in steps))
    root = DimensionTreeNode(False, max_bound)

    for action, bound in steps:
        root.partition(action, bound)

    return root
