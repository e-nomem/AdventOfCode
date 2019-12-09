from typing import List


def load_program_from_string(data: str) -> List[int]:
    return [int(i) for i in data.strip().split(',')]
