from math import ceil
from math import floor
from typing import cast
from typing import Optional
from typing import Union

# Can't do recursive type definitions :(
Number = Union[int, tuple]


def parse(input: str) -> tuple[Number, int]:
    increment = 1  # The opening bracket
    if input[increment] == "[":
        left, l_consumed = parse(input[increment:])
        increment += l_consumed
    else:
        left = int(input[increment])
        increment += 1  # The actual value

    increment += 1  # The comma separator

    if input[increment] == "[":
        right, r_consumed = parse(input[increment:])
        increment += r_consumed
    else:
        right = int(input[increment])
        increment += 1  # the actual value

    increment += 1  # The closing bracket

    return (left, right), increment


def add_left(root: Number, n: Optional[int]) -> Number:
    if n is None:
        return root

    if isinstance(root, int):
        return root + n

    return (add_left(root[0], n), root[1])


def add_right(root: Number, n: Optional[int]) -> Number:
    if n is None:
        return root

    if isinstance(root, int):
        return root + n

    return (root[0], add_right(root[1], n))


def explode(n: Number, depth: int = 0) -> tuple[bool, Optional[int], Number, Optional[int]]:
    if isinstance(n, int):
        return False, None, n, None

    if depth >= 4:
        # Since we always 'shallow' up anything deeper than 4, left and right
        # are both guaranteed to be ints
        return True, cast(int, n[0]), 0, cast(int, n[1])

    a, b = n

    did_explode, left, a, right = explode(a, depth + 1)
    if did_explode:
        return True, left, (a, add_left(b, right)), None

    did_explode, left, b, right = explode(b, depth + 1)
    if did_explode:
        return True, None, (add_right(a, left), b), right

    return False, None, n, None


def split(n: Number) -> tuple[bool, Number]:
    if isinstance(n, int):
        if n >= 10:
            return True, (floor(n / 2), ceil(n / 2))

        return False, n

    a, b = n

    did_split, a = split(a)
    if did_split:
        return True, (a, b)

    did_split, b = split(b)
    return did_split, (a, b)


def add_numbers(a: Number, b: Number) -> Number:
    n: Number = (a, b)
    while True:
        # First explode
        did_change, _, n, _ = explode(n)
        if did_change:
            continue

        # Then split
        did_change, n = split(n)

        if not did_change:
            break

    return n


def magnitude(n: Number) -> int:
    if isinstance(n, int):
        return n

    return (3 * magnitude(n[0])) + (2 * magnitude(n[1]))
