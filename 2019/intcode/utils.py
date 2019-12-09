from typing import Dict

Program = Dict[int, int]


def load_program_from_string(data: str) -> Program:
    d = [int(i) for i in data.strip().split(',')]
    return dict(zip(range(len(d)), d))
