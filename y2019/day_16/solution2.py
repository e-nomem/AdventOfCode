import asyncio
from os import path


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        data = [int(c) for c in input_file.read().strip()]

        # Grab the message offset first
        message_offset = int("".join(str(v) for v in data[0:7]))

        if message_offset < len(data) // 2:
            raise RuntimeError("Must use general solution for part 1")

        # Extend the message
        data *= 10000

        # This process has an interesting pattern:
        # output[i] = sum(input[i+1:]) % 10 where len(input) // 2 <= i < len(input)
        # so this solution only works if the message is in the second half of the data
        data = data[message_offset:]
        data.reverse()

        for _ in range(100):
            val = 0
            for i in range(len(data)):
                val += data[i]
                data[i] = val % 10

        data.reverse()

        solution = "".join(str(v) for v in data[:8])
        print(f"Solution: {solution}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
