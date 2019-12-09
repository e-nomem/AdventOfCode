from enum import IntEnum
from typing import List

from .io import Reader
from .io import stdin
from .io import stdout
from .io import Writer


class ParameterMode(IntEnum):
    Position = 0
    Immediate = 1


class Opcode(IntEnum):
    Add = 1
    Multiply = 2
    Input = 3
    Output = 4
    JmpIfTrue = 5
    JmpIfFalse = 6
    LessThan = 7
    Equals = 8
    Halt = 99


async def run_program(prog: List[int], reader: Reader = stdin, writer: Writer = stdout) -> None:
    """
    Runs the provided program. The program will be mutated, so ensure that a copy is passed in if
    it should be reused/rerun multiple times
    """

    def opcode() -> Opcode:
        code = prog[ptr] % 100
        try:
            return Opcode(code)
        except ValueError:
            raise RuntimeError(f"Unknown opcode '{code}' at index {ptr} ({prog[ptr]})")

    def get_mode(param: int) -> ParameterMode:
        mode = (prog[ptr] // (10 ** (param + 1))) % 10
        try:
            return ParameterMode(mode)
        except ValueError:
            raise RuntimeError(f"Unknown parameter mode '{mode}' at index {ptr} ({prog[ptr]})")

    def read(param: int) -> int:
        mode = get_mode(param)
        if mode == ParameterMode.Position:
            return prog[prog[ptr + param]]
        elif mode == ParameterMode.Immediate:
            return prog[ptr + param]
        else:
            raise NotImplementedError(f"Parameter mode '{mode.name}' ({mode.value}) not yet implemented")

    def write(param: int, value: int) -> None:
        mode = get_mode(param)
        if mode != ParameterMode.Position:
            raise RuntimeError(f'Output parameter mode must be Position. At index {ptr} ({prog[ptr]})')

        prog[prog[ptr + param]] = value

    ptr = 0
    read_iter = reader()

    # Main program loop starts here
    while True:
        instr = opcode()
        if instr == Opcode.Add:
            write(3, read(1) + read(2))
            ptr += 4
        elif instr == Opcode.Multiply:
            write(3, read(1) * read(2))
            ptr += 4
        elif instr == Opcode.Input:
            async for val in read_iter:
                # Read one value from input and break from the async generator
                write(1, val)
                break
            ptr += 2
        elif instr == Opcode.Output:
            # Write is async because it may need to acquire a lock
            await writer(read(1))
            ptr += 2
        elif instr == Opcode.JmpIfTrue:
            if read(1):
                ptr = read(2)
            else:
                ptr += 3
        elif instr == Opcode.JmpIfFalse:
            if not read(1):
                ptr = read(2)
            else:
                ptr += 3
        elif instr == Opcode.LessThan:
            val = 0
            if read(1) < read(2):
                val = 1
            write(3, val)
            ptr += 4
        elif instr == Opcode.Equals:
            val = 0
            if read(1) == read(2):
                val = 1
            write(3, val)
            ptr += 4
        elif instr == Opcode.Halt:
            return
        else:
            raise NotImplementedError(f"Opcode '{instr.name}' ({instr.value}) not yet implemented")
