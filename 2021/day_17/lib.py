from collections.abc import Iterator
from math import ceil
from math import sqrt
from typing import Optional


def launch(initial_v: tuple[int, int], x_range: tuple[int, int], y_range: tuple[int, int]) -> Optional[int]:
    max_y = 0
    x = 0
    y = 0
    dx, dy = initial_v

    while True:
        x += dx
        y += dy
        max_y = max(max_y, y)
        dy -= 1
        if dx != 0:
            dx += -1 if dx > 0 else 1

        if x_range[0] <= x <= x_range[1] and y_range[0] <= y <= y_range[1]:
            return max_y

        if dy < 0 and y < y_range[0]:
            return None

        if dx > 0 and x > x_range[1]:
            return None


def all_launches(x_range: tuple[int, int], y_range: tuple[int, int]) -> Iterator[int]:
    # Calculate the minimum x velocity that will reach our target
    # (x^2 + x) / 2 >= x_range[0]
    # x^2 + x >= 2 * x_range[0]
    # x^2 + x + (-2 * x_range[0]) >= 0
    # via quadratic equation
    # a = 1, b = 1, c = -2 * x_range[0]
    # x = (-b +/- sqrt(b ** 2 - 4 * a * c) / (2 * a)
    # Solve for just the positive root
    # x = (-1 + sqrt((1 ** 2) - (4 * 1 * -2 * x_range[0]))) / (2 * 1)
    # x = (-1 + sqrt(1 + (8 * x_range[0]))) / 2
    min_x = ceil((sqrt(1 + (8 * x_range[0])) - 1) / 2)

    # We can use -y_range[0] as the maximum y velocity because it will hit the ground (y=0) at the same but opposite velocity
    # and _just_ barely hit the last row of our target. Any higher initial y velocity will skip our target entirely on the
    # way down.
    sim_launches = (
        launch((dx, dy), x_range, y_range)
        for dx in range(min_x, x_range[1] + 1)
        for dy in range(y_range[0], 1 - y_range[0])
    )
    return (height for height in sim_launches if height is not None)
