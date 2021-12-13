import asyncio
from collections import defaultdict
from os import path


def fold(dots: set[tuple[int, int]], direction: str, border: int, maxes: tuple[int, int]) -> tuple[int, int]:
    if direction == 'x':
        min_x = border + 1
        min_y = 0
        for y in range(0, maxes[1] + 1):
            if (border, y) in dots:
                dots.remove((border, y))
    else:
        min_x = 0
        min_y = border + 1
        for x in range(0, maxes[0] + 1):
            if (x, border) in dots:
                dots.remove((x, border))

    for x in range(min_x, maxes[0] + 1):
        for y in range(min_y, maxes[1] + 1):
            if (x, y) in dots:
                if direction == 'x':
                    shift_x = border - (x - border)
                    dots.add((shift_x, y))
                else:
                    shift_y = border - (y - border)
                    dots.add((x, shift_y))

                dots.remove((x, y))

    if direction == 'x':
        return (border - 1, maxes[1])
    else:
        return (maxes[0], border - 1)


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, 'input.txt')
    with open(infile) as input_file:
        dots: set[tuple[int, int]] = set()
        for line in input_file:
            line = line.strip()
            if not line:
                break

            x_str, y_str = line.split(',')
            dots.add((int(x_str), int(y_str)))

        maxes = (0, 0)
        for dot in dots:
            x, y = dot
            if x > maxes[0]:
                maxes = (x, maxes[1])
            if y > maxes[1]:
                maxes = (maxes[0], y)

        for line in input_file:
            line = line.strip()
            parts = line.split(' ')[2].split('=')
            direction = parts[0]
            border = int(parts[1])
            maxes = fold(dots, direction, border, maxes)
            break

    print(len(dots))


if __name__ == '__main__':
    asyncio.run(main())
