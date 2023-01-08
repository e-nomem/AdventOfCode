import asyncio
from os import path
from typing import List


def read_layers(data: str, x_size: int = 25, y_size: int = 6) -> list[str]:
    layer_size = x_size * y_size
    layer_count = len(data) // layer_size
    return [data[i * layer_size : layer_size + i * layer_size] for i in range(layer_count)]


def solve(layers: list[str]) -> int:
    min_layer = min(layers, key=lambda i: i.count("0"))
    return min_layer.count("1") * min_layer.count("2")


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        layers = read_layers(input_file.read().strip())
        print(f"Solution: {solve(layers)}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
