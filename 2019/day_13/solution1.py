import asyncio
from os import path
from typing import Callable
from typing import Optional
from typing import Tuple

from ..intcode.executor import run
from ..intcode.io import Writer
from ..intcode.utils import load
from ..util.image import ImageBuf
from ..util.image import Pixel
from ..util.point import Point

OBJECTS = {
    0: ' ',
    1: '#',
    2: '=',
    3: '_',
    4: 'o',
}


def image_capture() -> Tuple[Writer, Callable[[], ImageBuf]]:
    x: Optional[int] = None
    y: Optional[int] = None

    buffer: ImageBuf = set()

    async def writer(val: int) -> None:
        nonlocal x
        nonlocal y
        if x is None:
            x = val
        elif y is None:
            y = val
        else:
            point = Point(x, y)
            pixel = Pixel(point, OBJECTS[val])
            buffer.add(pixel)
            x = None
            y = None

    def get_image() -> ImageBuf:
        return buffer

    return writer, get_image


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, 'input.txt')
    with open(infile, 'r') as input_file:
        writer, get_buffer = image_capture()
        prog = load(input_file.read())
        await run(prog, writer=writer)

        buffer = get_buffer()
        blocks = sum(1 for p in buffer if p.char == OBJECTS[2])
        print(f'Solution: {blocks}')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
