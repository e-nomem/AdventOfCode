import asyncio
from unittest.mock import patch

import pytest

from .io import concat
from .io import pipe
from .io import repeat
from .io import static
from .io import stdin
from .io import stdout
from .io import tee

# Mark all tests in this module as async
pytestmark = pytest.mark.asyncio


async def test_tee() -> None:
    o1 = -1
    o2 = -1

    async def w1(val: int) -> None:
        nonlocal o1
        o1 = val

    async def w2(val: int) -> None:
        nonlocal o2
        o2 = val

    combined = tee(w1, w2)

    await combined(42)
    assert o1 == 42
    assert o2 == 42


async def test_static() -> None:
    reader = static(0, 1, 2, 3, 4)

    i = 0
    read_iter = reader()
    async for val in read_iter:
        assert val == i
        i += 1

    assert i == 5


async def test_repeat() -> None:
    reader = repeat(42)

    i = 0
    read_iter = reader()
    async for val in read_iter:
        assert val == 42
        i += 1
        if i == 1000:
            break


async def test_concat() -> None:
    reader = concat(static(0, 1, 2), static(3, 4))

    i = 0
    read_iter = reader()
    async for val in read_iter:
        assert val == i
        i += 1

    assert i == 5


async def test_concat__infinite() -> None:
    reader = concat(static(0, 1, 2), repeat(42))

    i = 0
    read_iter = reader()
    async for val in read_iter:
        assert val == i
        i += 1
        if i == 3:
            break

    # Switch from the static to repeat input
    async for val in read_iter:
        assert val == 42
        i += 1
        if i == 1000:
            break


@pytest.mark.timeout(0.1)
async def test_pipe_init_data() -> None:
    reader, _ = pipe(0, 1, 2)

    i = 0
    read_iter = reader()
    async for val in read_iter:
        assert val == i
        i += 1
        if i == 3:
            break


@pytest.mark.timeout(0.1)
async def test_pipe_write_read() -> None:
    reader, writer = pipe()

    await writer(0)
    await writer(1)
    await writer(2)

    i = 0
    read_iter = reader()
    async for val in read_iter:
        assert val == i
        i += 1
        if i == 3:
            break


@pytest.mark.timeout(1)
async def test_pipe_read_block() -> None:
    reader, writer = pipe()

    i = 0
    read_iter = reader()

    async def _inner() -> None:
        nonlocal i
        async for val in read_iter:
            assert val == i
            i += 1
            if i == 3:
                break

    coro = _inner()
    await asyncio.sleep(0.5)
    await writer(0)
    await writer(1)
    await writer(2)
    await coro
    assert i == 3


async def test_stdout() -> None:
    with patch("builtins.print") as mock_print:
        await stdout(42)
        mock_print.assert_called_with("(output)> 42")
        mock_print.assert_called_once()


async def test_stdin() -> None:
    with patch("builtins.input", lambda _: "42"):
        read_iter = stdin()

        async for val in read_iter:
            assert val == 42
            break
