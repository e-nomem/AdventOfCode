import asyncio
from os import path
from typing import List


def read_layers(data: str, x_size: int = 25, y_size: int = 6) -> List[str]:
    layer_size = x_size * y_size
    layer_count = len(data) // layer_size
    return [
        data[i * layer_size:layer_size + i * layer_size] for i in range(layer_count)
    ]


def print_image(layers: List[str], x_size: int = 25, y_size: int = 6) -> None:
    for y in range(y_size):
        for x in range(x_size):
            idx = (y * x_size) + x
            for layer in layers:
                if layer[idx] != '2':
                    print(layer[idx].replace('0', ' '), end='')
                    break
        print()


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, 'input.txt')
    with open(infile, 'r') as input_file:
        layers = read_layers(input_file.read().strip())
        print_image(layers)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
