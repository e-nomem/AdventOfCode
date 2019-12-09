from os import path
from typing import Set


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f'({self.x}, {self.y})'


def process_path(pathspec: str) -> Set[Point]:
    points: Set[Point] = set()
    x = 0
    y = 0
    for command in pathspec.split(','):
        direction, *rest = command
        distance = int(''.join(rest))
        for _ in range(distance):
            if direction == 'U':
                y += 1
            elif direction == 'D':
                y -= 1
            elif direction == 'R':
                x += 1
            elif direction == 'L':
                x -= 1
            else:
                raise RuntimeError(f"Unknown direction '{direction}'")
            points.add(Point(x, y))

    return points


def distance(point: Point) -> int:
    return abs(point.x) + abs(point.y)


def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, 'input.txt')
    with open(infile, 'r') as input_file:
        paths = [process_path(line) for line in input_file]
        intersections = set(paths[0]).intersection(paths[1])

        min_distance = min(distance(p) for p in intersections)
        print(f'Minimum Distance: {min_distance}')


if __name__ == '__main__':
    main()
