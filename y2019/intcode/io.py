import asyncio
from collections import deque
from collections.abc import AsyncGenerator
from collections.abc import Awaitable
from collections.abc import Callable
from typing import Tuple

Reader = Callable[[], AsyncGenerator[int, None]]
Writer = Callable[[int], Awaitable[None]]


async def stdin() -> AsyncGenerator[int, None]:
    """
    Default Reader implementation that prompts for input on STDIN
    """
    while True:
        yield int(input("(input)> "))


async def stdout(val: int) -> None:
    """
    Default Writer implementation that prints to STDOUT
    """
    print(f"(output)> {val}")


def repeat(val: int) -> Reader:
    """
    Creates a reader that will repeat the same input
    """

    async def _helper() -> AsyncGenerator[int, None]:
        while True:
            yield val

    return _helper


def static(*init: int) -> Reader:
    """
    Creates a Reader that will return static data
    """

    async def _helper() -> AsyncGenerator[int, None]:
        for data in reversed(init):
            yield data

    return _helper


def concat(*readers: Reader) -> Reader:
    """
    Takes in multiple Readers and returns a Reader that will read from them sequentially
    """

    async def _helper() -> AsyncGenerator[int, None]:
        for reader in readers:
            read_iter = reader()
            async for val in read_iter:
                yield val

    return _helper


def pipe(*init: int) -> tuple[Reader, Writer]:
    """
    Provides a Reader/Writer pair that are connected to each other so that multiple programs
    can be connected together
    """
    buffer = deque(init)
    cond = asyncio.Condition()

    async def reader() -> AsyncGenerator[int, None]:
        while True:
            async with cond:
                while len(buffer) == 0:
                    await cond.wait()
                yield buffer.popleft()

    async def writer(val: int) -> None:
        async with cond:
            buffer.append(val)
            cond.notify_all()

    return reader, writer


def tee(*writers: Writer) -> Writer:
    """
    Takes in multiple writers and returns a writer that will write to all of them
    """

    async def _helper(val: int) -> None:
        await asyncio.wait([asyncio.create_task(w(val)) for w in writers], return_when=asyncio.ALL_COMPLETED)

    return _helper
