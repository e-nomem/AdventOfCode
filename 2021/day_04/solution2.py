import asyncio
from itertools import chain
from os import path

Board = list[list[int]]


def is_winning_board(selected: set[int], board: Board) -> bool:
    for row in board:
        if all(v in selected for v in row):
            return True

    for col in range(len(board[0])):
        if all(r[col] in selected for r in board):
            return True

    return False


def find_losing_board(numbers: list[int], boards: list[Board]) -> tuple[Board, set[int], int]:
    selected = set(numbers[:4])
    won_boards = set()

    for i in numbers[4:]:
        selected.add(i)
        for bidx, board in enumerate(boards):
            if bidx in won_boards:
                continue

            if is_winning_board(selected, board):
                won_boards.add(bidx)

            if len(won_boards) == len(boards):
                return board, selected, i


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, 'input.txt')
    boards: list[Board] = []
    with open(infile) as input_file:
        lines = (line.strip() for line in input_file)
        numbers = [int(i) for i in next(lines).split(',')]
        for line in lines:
            if not line:
                boards.append([])
                continue

            boards[-1].append([int(i) for i in line.split(' ') if i])

    board, selected, final = find_losing_board(numbers, boards)

    unselected = sum(v for row in board for v in row if v not in selected)
    print(unselected * final)




if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
