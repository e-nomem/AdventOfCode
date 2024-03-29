from typing import List


def password_is_valid(password: str) -> bool:
    if len(password) != 6:
        return False

    if len(set(password)) == 6:
        return False

    val = int(password[0])
    for c in password:
        if int(c) < val:
            return False
        val = int(c)

    return True


def possible_passwords(start: int, end: int) -> list[int]:
    return [p for p in range(start, end + 1) if password_is_valid(str(p))]


def main() -> None:
    passwords = possible_passwords(124075, 580769)
    print(f"Possible Password Count: {len(passwords)}")


if __name__ == "__main__":
    main()
