from os import path


def calc_fuel(mass: int) -> int:
    return (mass // 3) - 2


def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        modules = [int(line.strip()) for line in input_file]
        print(f"Solution: {sum(map(calc_fuel, modules))}")


if __name__ == "__main__":
    main()
