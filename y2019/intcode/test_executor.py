from collections.abc import AsyncGenerator

import pytest

from .executor import run
from .utils import load

# Mark all tests in this module as async
pytestmark = pytest.mark.asyncio


async def test_out_of_range_read() -> None:
    s = "2,0,15,5,99,1"
    p = load(s)

    assert len(p) == 6
    assert await run(p) == 4
    assert p[5] == 0  # p[1] * p[15] = 2 * 0


async def test_negative_mem_read() -> None:
    s = "109,-15,201,0,0,0,99"
    p = load(s)

    with pytest.raises(RuntimeError) as e:
        await run(p)

    assert str(e.value).startswith("Cannot read from negative pointer")


async def test_out_of_range_write() -> None:
    s = "2,0,0,20,99"
    p = load(s)

    assert len(p) == 5
    assert await run(p) == 4
    assert p[19] == 0  # Unset memory location
    assert p[20] == 4  # Out of range write


async def test_negative_mem_write() -> None:
    s = "109,-15,21101,1,1,0,99"
    p = load(s)

    with pytest.raises(RuntimeError) as e:
        await run(p)

    assert str(e.value).startswith("Cannot write to negative pointer")


async def test_unknown_opcode() -> None:
    s = "98"
    p = load(s)

    with pytest.raises(RuntimeError) as e:
        await run(p)

    assert str(e.value).startswith("Unknown opcode")


async def test_unknown_param_mode() -> None:
    s = "901"
    p = load(s)

    with pytest.raises(RuntimeError) as e:
        await run(p)

    assert str(e.value).startswith("Unknown parameter mode")


async def test_read_param_immediate() -> None:
    s = "1101,15,25,5,99,0"
    p = load(s)

    assert len(p) == 6
    assert await run(p) == 4
    assert p[5] == 40


async def test_write_param_immediate() -> None:
    s = "10001,1,1,1,99"
    p = load(s)

    with pytest.raises(NotImplementedError) as e:
        await run(p)

    assert str(e.value).startswith("Output parameter in mode")


async def test_halt() -> None:
    s = "99"
    p = load(s)

    assert len(p) == 1
    assert await run(p) == 0


async def test_add() -> None:
    s = "1,0,0,5,99,0"
    p = load(s)

    assert len(p) == 6
    assert await run(p) == 4
    assert p[5] == 2


async def test_multiply() -> None:
    s = "2,0,2,5,99,0"
    p = load(s)

    assert len(p) == 6
    assert await run(p) == 4
    assert p[5] == 4


async def test_input() -> None:
    s = "3,1,99"
    p = load(s)

    async def provider() -> AsyncGenerator[int, None]:
        yield 42

    assert await run(p, reader=provider) == 2
    assert p[1] == 42


async def test_input__exhausted() -> None:
    s = "3,1,3,3"
    p = load(s)

    async def provider() -> AsyncGenerator[int, None]:
        yield 42

    with pytest.raises(RuntimeError) as e:
        await run(p, reader=provider)

    assert str(e.value) == "Input exhausted"
    assert p[1] == 42
    assert p[3] == 3


async def test_output() -> None:
    s = "104,42,99"
    p = load(s)
    output = 0

    async def save(val: int) -> None:
        nonlocal output
        output = val

    assert await run(p, writer=save) == 2
    assert output == 42


async def test_jump_if_true() -> None:
    s = "1105,1,6,99,0,0,99"
    p = load(s)

    assert len(p) == 7
    assert await run(p) == 6


async def test_jump_if_true__false() -> None:
    s = "1105,0,6,99,0,0,99"
    p = load(s)

    assert len(p) == 7
    assert await run(p) == 3


async def test_jump_if_true__negative() -> None:
    s = "1105,-20,-30,99"
    p = load(s)

    with pytest.raises(RuntimeError) as e:
        await run(p)

    assert str(e.value) == "Cannot run with negative pointer -30"


async def test_jump_if_false() -> None:
    s = "1106,0,6,99,0,0,99"
    p = load(s)

    assert len(p) == 7
    assert await run(p) == 6


async def test_jump_if_false__false() -> None:
    s = "1106,-15,6,99,0,0,99"
    p = load(s)

    assert len(p) == 7
    assert await run(p) == 3


async def test_jump_if_false__negative() -> None:
    s = "1106,0,-30,99"
    p = load(s)

    with pytest.raises(RuntimeError) as e:
        await run(p)

    assert str(e.value) == "Cannot run with negative pointer -30"


async def test_less_than() -> None:
    s = "1107,-5,0,0,99"
    p = load(s)

    assert len(p) == 5
    assert await run(p) == 4
    assert p[0] == 1


async def test_less_than__false() -> None:
    s = "107,-5,5,0,99,-15"
    p = load(s)

    assert len(p) == 6
    assert await run(p) == 4
    assert p[0] == 0


async def test_equals() -> None:
    s = "1108,-5,-5,0,99"
    p = load(s)

    assert len(p) == 5
    assert await run(p) == 4
    assert p[0] == 1


async def test_equals__false() -> None:
    s = "108,0,5,0,99,-15"
    p = load(s)

    assert len(p) == 6
    assert await run(p) == 4
    assert p[0] == 0


async def test_set_rel_base() -> None:
    s = "109,7,22101,15,0,1,99,17,10"
    p = load(s)

    assert await run(p) == 6
    assert p[8] == 32


async def test_set_rel_base__negative() -> None:
    s = "109,-15,22101,15,22,23,99,17,10"
    p = load(s)

    assert await run(p) == 6
    assert p[8] == 32
