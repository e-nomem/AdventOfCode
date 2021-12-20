Image = list[list[int]]
Algorithm = tuple[int, ...]


def calc_point(
    image: Image,
    algorithm: Algorithm,
    point: tuple[int, int],
    blank: int,
    maxes: tuple[int, int],
) -> int:
    num = 0
    for y in range(point[1] - 1, point[1] + 2):
        for x in range(point[0] - 1, point[0] + 2):
            num <<= 1
            if 0 <= x < maxes[0] and 0 <= y < maxes[1]:
                num |= image[y][x]
            else:
                num |= blank

    return algorithm[num]


def expand_image(data: tuple[Image, Algorithm], step: int) -> tuple[Image, Algorithm]:
    image, algorithm = data
    max_x = len(image[0])
    max_y = len(image)

    needs_alternate = algorithm[0] == 1 and algorithm[-1] == 0
    blank = step % 2 if needs_alternate else 0

    new_image: list[list[int]] = []

    for y in range(-1, max_y + 1):
        new_image.append([])
        for x in range(-1, max_x + 1):
            new_image[-1].append(calc_point(image, algorithm, (x, y), blank, (max_x, max_y)))

    return new_image, algorithm


def count_lights(image: Image) -> int:
    return sum(val for row in image for val in row)
