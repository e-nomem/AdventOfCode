from os import path


def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        numbers = [int(i.strip()) for i in input_file]
        for i in range(len(numbers)):
            for j in range(i, len(numbers)):
                if numbers[i] + numbers[j] == 2020:
                    print(numbers[i] * numbers[j])
                    return


if __name__ == "__main__":
    main()
