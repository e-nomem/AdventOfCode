from collections import defaultdict
from typing import Dict

Program = Dict[int, int]


def load_program_from_string(data: str) -> Program:
    d = [int(i) for i in data.strip().split(',')]
    return defaultdict(int, enumerate(d))
