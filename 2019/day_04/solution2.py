from typing import Dict
from typing import List


def password_is_valid(password: str) -> bool:
    if len(password) != 6:
        return False

    if len(set(password)) == 6:
        return False

    val = int(password[0])
    dup_count: Dict[str, int] = {}
    for c in password[1:]:
        if int(c) < val:
            return False
        elif int(c) == val:
            dups = dup_count.get(c, 0)
            dup_count[c] = dups + 1
        else:
            val = int(c)

    return bool([c for c, count in dup_count.items() if count == 1])


def possible_passwords(start: int, end: int) -> List[int]:
    return [p for p in range(start, end + 1) if password_is_valid(str(p))]


def main() -> None:
    passwords = possible_passwords(124075, 580769)
    print(f'Possible Password Count: {len(passwords)}')


if __name__ == '__main__':
    main()
