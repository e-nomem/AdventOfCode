import asyncio
from bisect import bisect_left
from os import path


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        numbers = list(sorted(line.strip() for line in input_file))
        low = 0
        high = len(numbers)
        for bit in range(len(numbers[0])):
            if high == low:
                break
            mid = low + ((high - low) // 2)
            switch_point = bisect_left(numbers, 1, low, high, key=lambda n: int(n[bit]))
            if switch_point > mid:
                # Most frequent bit is 0
                high = switch_point
            else:
                low = switch_point
        o2 = numbers[low]

        low = 0
        high = len(numbers)
        for bit in range(len(numbers[0])):
            if high == low:
                break
            mid = low + ((high - low) // 2)
            switch_point = bisect_left(numbers, 1, low, high, key=lambda n: int(n[bit]))
            if switch_point > mid:
                # Most frequent bit is 0
                low = switch_point
            else:
                high = switch_point
        co2 = numbers[low]

        # print(o2)
        # print(co2)
        print(int(o2, 2) * int(co2, 2))


if __name__ == "__main__":
    asyncio.run(main())
