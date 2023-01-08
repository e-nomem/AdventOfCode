from os import path
from typing import List


def is_valid(input_str: str) -> bool:
    policy, password = input_str.split(":", 1)
    password = password.strip()
    repeat, char = policy.split(" ", 1)
    min_index, max_index = repeat.split("-", 1)
    c1 = password[int(min_index) - 1]
    c2 = password[int(max_index) - 1]
    print(
        f"Pass: {password}, Seek: {char}, LI: {min_index}, MI: {max_index}, C1: {c1}, C2: {c2}, Valid: {(c1 == char or c2 == char) and c1 != c2}",
    )
    return (c1 == char or c2 == char) and c1 != c2


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
