from os import path


def calc_fuel(mass: int) -> int:
    return (mass // 3) - 2


def module_fuel(mass: int) -> int:
    fuel_added = calc_fuel(mass)
    fuel_needed = 0

    while fuel_added > 0:
        fuel_needed += fuel_added
        fuel_added = calc_fuel(fuel_added)

    return fuel_needed


def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        modules = [int(line.strip()) for line in input_file]
        print(f"Solution: {sum(map(module_fuel, modules))}")


if __name__ == "__main__":
    main()
