import asyncio
from math import copysign
from os import path

from aoclib.timing import benchmark


def move_tail(head_pos: tuple[int, int], tail_pos: tuple[int, int]) -> tuple[int, int]:
    h_x, h_y = head_pos
    t_x, t_y = tail_pos
    for x_dir in range(-1, 2):
        for y_dir in range(-1, 2):
            if t_x + x_dir == h_x and t_y + y_dir == h_y:
                # Within 1 of head, no need to move
                return tail_pos

    if h_x == t_x:
        dir = int(copysign(1, h_y - t_y))
        return t_x, t_y + dir
    if h_y == t_y:
        dir = int(copysign(1, h_x - t_x))
        return t_x + dir, t_y

    # Not on same row or column, need to move diagonally
    # There are only 4 diagonal destinations for the tail, and each one covers
    # 3 possible head positions
    for x_dir in range(-1, 2, 2):
        for y_dir in range(-1, 2, 2):
            if (
                (h_x == t_x + (2 * x_dir) and h_y == t_y + y_dir)
                or (h_x == t_x + x_dir and h_y == t_y + (2 * y_dir))
                or (h_x == t_x + (2 * x_dir) and h_y == t_y + (2 * y_dir))
            ):
                return t_x + x_dir, t_y + y_dir

    raise Exception(f"Failed to find tail pos {head_pos=}, {tail_pos=}")


@benchmark(10)
def puzzle(input_lines: list[str]) -> None:
    positions: set[tuple[int, int]] = set()
    knots: list[tuple[int, int]] = [(0, 0) for _ in range(2)]

    for line in input_lines:
        dir, mag = line.split()
        mag = int(mag)
        x_dir = 0
        y_dir = 0
        match dir:
            case "R":
                x_dir = 1
            case "L":
                x_dir = -1
            case "U":
                y_dir = 1
            case "D":
                y_dir = -1

        for _ in range(mag):
            head_pos = knots[0]
            knots[0] = (head_pos[0] + x_dir, head_pos[1] + y_dir)
            for i in range(1, len(knots)):
                knots[i] = move_tail(knots[i - 1], knots[i])
            positions.add(knots[-1])

    print(len(positions))


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l.strip() for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
