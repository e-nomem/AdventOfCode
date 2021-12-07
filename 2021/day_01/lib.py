from collections import deque
from typing import Generator
from typing import Iterable
from typing import TypeVar

_T = TypeVar('_T')


def window(inp: Iterable[_T], n: int = 2) -> Generator[tuple[_T, ...], None, None]:
    if n < 1:
        raise ValueError('Window size must be greater than 0')

    it = iter(inp)
    buf: deque[_T] = deque(maxlen=n)

    # Fill the buf with n-1 items
    try:
        for _ in range(n - 1):
            buf.append(next(it))
    except StopIteration:
        # We exhausted the iterator before filling the buffer
        # This is ok because we will never yield anything
        # Since the input is smaller than the window size
        pass

    # Consume the rest of the iterator, yielding tuple windows
    for i in it:
        buf.append(i)
        yield tuple(buf)
