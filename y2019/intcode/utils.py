from collections import defaultdict
from typing import Dict

Program = dict[int, int]


def load(data: str) -> Program:
    d = (int(i) for i in data.strip().split(",") if i)
    return defaultdict(int, enumerate(d))
