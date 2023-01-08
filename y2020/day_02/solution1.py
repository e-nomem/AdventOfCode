from os import path
from typing import List


def is_valid(input_str: str) -> bool:
    policy, password = input_str.split(":", 1)
    password = password.strip()
    repeat, char = policy.split(" ", 1)
    min_count, max_count = repeat.split("-", 1)
    return int(min_count) <= len([c for c in password if c == char]) <= int(max_count)


def num_valid(inputs: list[str]) -> int:
    return len([i for i in inputs if is_valid(i)])


def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        inputs = [i.strip() for i in input_file]
        valid_count = num_valid(inputs)
        print(valid_count)


if __name__ == "__main__":
    main()
