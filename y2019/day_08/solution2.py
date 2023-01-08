import asyncio
from os import path
from typing import List

from ..util import ImageBuf
from ..util import Point
from ..util import print_image


def read_layers(data: str, x_size: int = 25, y_size: int = 6) -> list[str]:
    layer_size = x_size * y_size
    layer_count = len(data) // layer_size
    return [data[i * layer_size : layer_size + i * layer_size] for i in range(layer_count)]


def merge_layers(layers: list[str], x_size: int = 25, y_size: int = 6) -> ImageBuf:
    points = set()
    for y in range(y_size):
        for x in range(x_size):
            idx = (y * x_size) + x
            for layer in layers:
                if layer[idx] != "2":
                    if layer[idx] == "1":
                        points.add(Point(x, -y))
                    break
    return points


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        layers = read_layers(input_file.read().strip())
        merged = merge_layers(layers)
        print_image(merged)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
