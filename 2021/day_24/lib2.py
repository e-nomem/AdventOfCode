from collections.abc import Callable
from collections.abc import Generator
from collections.abc import Iterable

from .lib import BLOCK_SIZE
from .lib import extract_params
from .lib import Program

Constraint = Callable[[tuple[int, ...], int], bool]
InputGenerator = Callable[[tuple[int, ...]], Iterable[int]]
ValueGenerator = Callable[[tuple[int, ...]], Iterable[int]]


# Input generators
def all_inputs() -> InputGenerator:
    return lambda _: tuple(i for i in range(1, 10))


def exact_input(index: int, offset: int) -> InputGenerator:
    return lambda vals: (vals[index] + offset,)


# Constraints
def is_valid(_: tuple[int, ...], n: int) -> bool:
    return 0 < n <= 9


def shift(offset: int) -> Constraint:
    return lambda vals, n: is_valid(vals, n + offset)


def exact(index: int, offset: int) -> Constraint:
    return lambda vals, n: n == vals[index] + offset


# Value generators
def constrained_values(inputs: InputGenerator, *constraints: Constraint) -> ValueGenerator:
    return lambda vals: tuple(i for i in inputs(vals) if all(c(vals, i) for c in constraints))


# Special case for exact values since we don't need to iterate over all the possible inputs
def exact_value(index: int, offset: int, *constraints: Constraint) -> ValueGenerator:
    return lambda vals: constrained_values(exact_input(index, offset), exact(index, offset), *constraints)(vals)


def make_value_generators(program: Program) -> Iterable[ValueGenerator]:
    stack: list[tuple[int, int]] = []
    generators: dict[int, ValueGenerator] = {}
    for i, idx in enumerate(range(0, len(program), BLOCK_SIZE)):
        params = extract_params(program[idx : idx + BLOCK_SIZE])
        if params[0] == 1:
            stack.append((i, params[2]))
        else:
            prev_push = stack.pop()
            offset = prev_push[1] + params[1]
            generators[i] = exact_value(prev_push[0], offset, is_valid)
            generators[prev_push[0]] = constrained_values(all_inputs(), shift(offset), is_valid)

    return tuple(generators[i] for i in range(len(generators)))
