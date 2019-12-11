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
