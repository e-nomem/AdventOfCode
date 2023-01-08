from collections.abc import Generator
from collections.abc import Iterable
from collections.abc import Iterator
from itertools import islice
from typing import TypeVar

T = TypeVar("T")


def windowed(n: int, iterable: Iterable[T]) -> Generator[tuple[T, ...], None, None]:
    if n < 1:
        raise ValueError(f"window size must be greater than 0, got {n}")

    it = iter(iterable)

    res = tuple(islice(it, n))
    if len(res) == n:
        yield res

    for elem in it:
        res = res[1:] + (elem,)
        yield res


def chunked(n: int, iterable: Iterable[T]) -> Iterator[tuple[T, ...]]:
    if n < 1:
        raise ValueError(f"chunk size must be greater than 0, got {n}")

    it = iter(iterable)
    return iter(lambda: tuple(islice(it, n)), ())


def take(n: int, iterable: Iterable[T]) -> Generator[T, None, None]:
    if n < 0:
        raise ValueError(f"take size cannot be negative, got {n}")

    it = iter(iterable)
    for _ in range(n):
        yield next(it)
