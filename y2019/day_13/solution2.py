import asyncio
from collections.abc import AsyncGenerator
from collections.abc import Callable
from os import path
from typing import Optional
from typing import Tuple

from ..intcode.executor import run
from ..intcode.io import Reader
from ..intcode.io import Writer
from ..intcode.utils import load
from ..util.image import ImageBuf
from ..util.image import Pixel
from ..util.point import Point

OBJECTS = {
    0: " ",
    1: "#",
    2: "=",
    3: "_",
    4: "o",
}


def image_capture() -> tuple[Reader, Writer, Callable[[], int]]:
    x: Optional[int] = None
    y: Optional[int] = None

    score: int = 0
    buffer: ImageBuf = set()
    paddle_pos = Point(0, 0)
    ball_pos = Point(0, 0)

    async def _reader() -> AsyncGenerator[int, None]:
        while True:
            if ball_pos.x > paddle_pos.x:
                yield 1
            elif ball_pos.x < paddle_pos.x:
                yield -1
            else:
                yield 0

    async def _writer(val: int) -> None:
        nonlocal x
        nonlocal y
        nonlocal score
        nonlocal paddle_pos
        nonlocal ball_pos
        if x is None:
            x = val
        elif y is None:
            y = val
        else:
            if x == -1 and y == 0:
                score = val
            else:
                point = Point(x, y)
                pixel = Pixel(point, OBJECTS[val])
                buffer.add(pixel)
                if val == 3:
                    paddle_pos = point
                elif val == 4:
                    ball_pos = point

            x = None
            y = None

    def get_score() -> int:
        return score

    return _reader, _writer, get_score


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        reader, writer, get_score = image_capture()
        prog = load(input_file.read())
        prog[0] = 2
        await run(prog, reader=reader, writer=writer)

        print(f"Solution: {get_score()}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
