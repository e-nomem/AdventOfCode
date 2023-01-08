import asyncio
from functools import reduce
from itertools import cycle
from itertools import islice
from os import path

# SIZE = 10
SIZE = 10007
# SIZE = 119315717514047

INCREMENT_TO_JUMP_MAP = {}


def calculate_jump(increment):
    count = 1
    idx = increment
    while idx > 1:
        jumps = ((SIZE - idx) // increment) + 1
        count += jumps
        idx = (idx + (jumps * increment)) % SIZE

    return count


def process(state, shuffle):
    parts = shuffle.split(" ")
    is_forward = state[0]
    index = state[1]
    deck = state[2]
    if parts[1] == "into":
        index -= 1 if is_forward else -1
        is_forward = not is_forward
    elif parts[1] == "with":
        increment = int(parts[3])
        jump = INCREMENT_TO_JUMP_MAP[increment]
        jump *= 1 if is_forward else -1
        old_deck = deck[:]
        for i in range(SIZE):
            if index < 0:
                index += SIZE
            elif index >= SIZE:
                index -= SIZE
            deck[i] = old_deck[index]
            index += jump

        index = 0
        is_forward = True
    else:
        shift = int(parts[1])
        index += shift * (1 if is_forward else -1)

    if index < 0:
        index += SIZE
    elif index >= SIZE:
        index -= SIZE

    # print(f'{deck}')
    # print(f'Head: {index}, Forward: {is_forward}')
    # print()
    return (is_forward, index, deck)


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        lines = [line.strip() for line in input_file]
        # lines = [
        #     'deal into new stack',
        #     'cut -2',
        #     'deal with increment 7',
        #     'cut 8',
        #     'cut -4',
        #     'deal with increment 7',
        #     'cut 3',
        #     'deal with increment 9',
        #     'deal with increment 3',
        #     'cut -1',
        # ]

        # Precompute jumps for increments we have
        for line in lines:
            if "increment" in line:
                increment = int(line.split(" ")[3])
                if increment not in INCREMENT_TO_JUMP_MAP:
                    jump = calculate_jump(increment)
                    INCREMENT_TO_JUMP_MAP[increment] = jump
                    # print(f'Calculated jump for increment {increment} -> {jump}')
                # else:
                # print(f'Already calculated jump for increement {increment}')

        deck = list(range(SIZE))
        initial_state = (True, 0, deck)
        is_forward, head, final_deck = reduce(process, lines, initial_state)

        print("Flattening final state into proper dict")
        processed_deck = final_deck[:]
        for i in range(SIZE):
            offset = head + (i * (1 if is_forward else -1))
            if offset < 0:
                offset += SIZE
            elif offset >= SIZE:
                offset -= SIZE
            processed_deck[i] = final_deck[offset]

        # print(processed_deck)
        for idx, val in enumerate(processed_deck):
            if val == 2019:
                print(idx)
                break


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
