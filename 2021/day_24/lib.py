from collections.abc import Callable
from collections.abc import Iterable
from typing import Optional

Program = tuple[tuple[str, ...], ...]
BlockParams = tuple[int, tuple[int, int, int]]
GuessGenerator = Callable[[], Iterable[int]]

BLOCK_SIZE = 18


def extract_params(prog: Program) -> tuple[int, int, int]:
    return (int(prog[4][2]), int(prog[5][2]), int(prog[15][2]))


def eval_digit(digit: int, params: BlockParams) -> int:
    z, inputs = params
    divide, x_add, y_add = inputs

    x = ((z % 26) + x_add) != digit
    z //= divide
    if x:
        z = (z * 26) + digit + y_add

    return z


def generate_guesses(params: BlockParams, guess_generator: GuessGenerator) -> Optional[Iterable[int]]:
    z, inputs = params
    divide, x_add, _ = inputs
    if divide == 1:
        return guess_generator()
    else:
        x = (z % 26) + x_add
        if 0 < x <= 9:
            return [x]

    return None


def find_model(
    prog: Program,
    guess_generator: GuessGenerator,
    idx: int = 0,
    z: int = 0,
    num_idx: int = 13,
) -> Optional[int]:
    block = prog[idx : idx + BLOCK_SIZE]
    params = (z, extract_params(block))

    guesses = generate_guesses(params, guess_generator)
    if guesses is None:
        return None

    last_digit = not bool(num_idx)

    for i in guesses:
        z = eval_digit(i, params)
        if last_digit and z == 0:
            return i
        elif not last_digit:
            res = find_model(prog, guess_generator, idx + BLOCK_SIZE, z, num_idx - 1)
            if res is not None:
                return (i * (10 ** num_idx)) + res

    return None
