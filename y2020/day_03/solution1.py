from os import path
from typing import List


def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        inputs = [i.strip() for i in input_file]


if __name__ == "__main__":
    main()
