import asyncio
from os import path

from lib.timing import benchmark


def launch(initial_v, x_range, y_range):
    max_y = 0
    x = 0
    y = 0
    dx, dy = initial_v

    max_x = ((dx ** 2) + dx) // 2
    if max_x < x_range[0]:
        # Insufficient x velocity to reach target zone
        return None

    for _ in range(200):
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

    # Unreachable
    return None


def brute_force(x_range, y_range):
    sim_launches = (launch((dx, dy), x_range, y_range) for dx in range(x_range[1]) for dy in range(y_range[0], 100))
    return max(max_y for max_y in sim_launches if max_y is not None)


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    x_range, y_range = (
        list(map(int, r.split("=")[1].split(".."))) for r in input_lines[0].strip().split(": ")[1].split(", ")
    )
    print(brute_force(x_range, y_range))


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
