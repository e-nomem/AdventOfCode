from typing import Set

from .point import Point

ImageBuf = set[Point]


def print_image(buffer: ImageBuf) -> None:
    min_x = min(p.x for p in buffer)
    max_x = max(p.x for p in buffer)
    min_y = min(p.y for p in buffer)
    max_y = max(p.y for p in buffer)

    for y in range(max_y, min_y - 1, -1):
        for x in range(min_x, max_x + 1):
            print("█" if Point(x, y) in buffer else " ", end="")
        print()
