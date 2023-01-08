from os import path
from typing import List
from typing import Optional


def input_to_prog(data: str) -> list[int]:
    return [int(part) for part in data.split(",")]


def opcode(val: int) -> int:
    return int(f"{val:04}"[-2:])


def read_value(ptr: int, param: int, prog: list[int]) -> int:
    mode = int(f"{prog[ptr]:04}"[(-2 - param)])
    if mode == 0:
        return prog[prog[ptr + param]]
    elif mode == 1:
        return prog[ptr + param]
    else:
        raise RuntimeError(f"Unknown parameter mode {mode} for parameter {param} at index {ptr}")


def write_value(ptr: int, param: int, value: int, prog: list[int]) -> None:
    prog[prog[ptr + param]] = value


def run_program(
    prog: list[int],
    noun: Optional[int] = None,
    verb: Optional[int] = None,
) -> int:
    if noun is not None:
        prog[1] = noun

    if verb is not None:
        prog[2] = verb

    ptr = 0
    while prog[ptr] != 99:
        code = opcode(prog[ptr])
        if code == 1:
            # Add
            v1 = read_value(ptr, 1, prog)
            v2 = read_value(ptr, 2, prog)
            write_value(ptr, 3, v1 + v2, prog)
            ptr += 4
        elif code == 2:
            # Multiply
            v1 = read_value(ptr, 1, prog)
            v2 = read_value(ptr, 2, prog)
            write_value(ptr, 3, v1 * v2, prog)
            ptr += 4
        elif code == 3:
            # Read input from stdin
            v1 = int(input("(input)> "))
            write_value(ptr, 1, v1, prog)
            ptr += 2
        elif code == 4:
            # Output to stdout
            v1 = read_value(ptr, 1, prog)
            print(f"(output)> {v1}")
            ptr += 2
        elif code == 5:
            # Jump if true
            v1 = read_value(ptr, 1, prog)
            if v1 != 0:
                ptr = read_value(ptr, 2, prog)
            else:
                ptr += 3
        elif code == 6:
            # Jump if false
            v1 = read_value(ptr, 1, prog)
            if v1 == 0:
                ptr = read_value(ptr, 2, prog)
            else:
                ptr += 3
        elif code == 7:
            # Less than
            v1 = read_value(ptr, 1, prog)
            v2 = read_value(ptr, 2, prog)
            val = 1 if v1 < v2 else 0
            write_value(ptr, 3, val, prog)
            ptr += 4
        elif code == 8:
            # Equals
            v1 = read_value(ptr, 1, prog)
            v2 = read_value(ptr, 2, prog)
            val = 1 if v1 == v2 else 0
            write_value(ptr, 3, val, prog)
            ptr += 4
        else:
            raise RuntimeError(f"Unknown opcode {prog[ptr]} at index {ptr}")

    return prog[0]


def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        init_state = input_to_prog(input_file.read())
        run_program(init_state.copy())


if __name__ == "__main__":
    main()
