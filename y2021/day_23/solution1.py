import asyncio
import heapq
import typing
from os import path

T = typing.TypeVar("T")

WAITING_AREAS = [(1, x) for x in [1, 2, 4, 6, 8, 10, 11]]

WAITING_ROW = 1
WAITING_COLS = [1, 2, 4, 6, 8, 10, 11]
COST = {"A": 1, "B": 10, "C": 100, "D": 1000}

ROOM_COLS = [3, 5, 7, 9]


def pdist1(from_loc: tuple[int, int], to_loc: tuple[int, int]) -> int:
    return abs(from_loc[0] - to_loc[0]) + abs(from_loc[1] - to_loc[1])


def dijkstra(
    from_node: T,
    expand: typing.Callable[[T], typing.Iterable[tuple[int, T]]],
    to_node: typing.Optional[T] = None,
    heuristic: typing.Optional[typing.Callable[[T], int]] = None,
) -> tuple[dict[T, int], dict[T, T]]:
    """
    expand should return an iterable of (dist, successor node) tuples.
    Returns (distances, parents).
    Use path_from_parents(parents, node) to get a path.
    """
    if heuristic is None:
        heuristic = lambda _: 0
    seen = set()  # type: typing.Set[T]
    g_values = {from_node: 0}  # type: typing.Dict[T, int]
    parents = {}  # type: typing.Dict[T, T]

    # (f, g, n)
    todo = [(0 + heuristic(from_node), 0, from_node)]  # type: typing.List[typing.Tuple[int, int, T]]

    while todo:
        _, g, node = heapq.heappop(todo)

        assert node in g_values
        assert g_values[node] <= g

        if node in seen:
            continue

        assert g_values[node] == g
        if to_node is not None and node == to_node:
            break
        seen.add(node)

        for cost, new_node in expand(node):
            new_g = g + cost
            if new_node not in g_values or new_g < g_values[new_node]:
                parents[new_node] = node
                g_values[new_node] = new_g
                heapq.heappush(todo, (new_g + heuristic(new_node), new_g, new_node))

    return (g_values, parents)


def puzzle(input_lines: list[str]) -> None:
    out = 0

    FINAL_NODE = ()

    COST = {"A": 1, "B": 10, "C": 100, "D": 1000}

    def expand(node):
        # (weight, node)
        out = []

        # node should store waiting areas + rooms
        cur_waitings, cur_rooms = node

        if all(all(chr(ord("A") + i) == x for x in room) for i, room in enumerate(cur_rooms)):
            return [(0, FINAL_NODE)]

        def is_blocked(col_1, col_2):
            if col_1 > col_2:
                col_1, col_2 = col_2, col_1
            for blocked_col in range(col_1 + 1, col_2):
                if blocked_col in WAITING_COLS and cur_waitings[WAITING_COLS.index(blocked_col)] != "":
                    return True
            return False

        for room_idx, room in enumerate(cur_rooms):
            # find the thing to move
            for room_position, to_move in enumerate(room):
                if to_move == "":
                    continue
                to_move_row = 2 + room_position
                break
            else:
                continue
            for waiting_idx, waiting_col in enumerate(WAITING_COLS):
                if cur_waitings[waiting_idx] == "":
                    if is_blocked(waiting_col, ROOM_COLS[room_idx]):
                        continue

                    # have this person move over there
                    new_waitings = list(cur_waitings)
                    new_rooms = list(map(list, cur_rooms))

                    cost = pdist1((to_move_row, ROOM_COLS[room_idx]), (WAITING_ROW, waiting_col)) * COST[to_move]
                    new_waitings[waiting_idx] = to_move
                    new_rooms[room_idx][room_position] = ""
                    out.append((cost, (tuple(new_waitings), tuple(map(tuple, new_rooms)))))

        # move from waiting to room
        for waiting_idx, waiting_col in enumerate(WAITING_COLS):
            # find the thing to move
            to_move = cur_waitings[waiting_idx]
            if to_move == "":
                continue
            target_room_idx = ord(to_move) - ord("A")
            target_room = cur_rooms[target_room_idx]
            # NEED to there
            if target_room[0] == "" and all(x == "" or x == to_move for x in target_room[1:]):
                # move in
                room_col = ROOM_COLS[target_room_idx]
                # go back
                for room_position in range(len(target_room))[::-1]:
                    if target_room[room_position] != "":
                        continue
                    room_row = room_position + 2
                    break
                else:
                    assert False

                if is_blocked(waiting_col, room_col):
                    continue

                cost = pdist1((room_row, room_col), (WAITING_ROW, waiting_col)) * COST[to_move]

                new_waitings = list(cur_waitings)
                new_rooms = [list(c) for c in cur_rooms]

                new_waitings[waiting_idx] = ""
                new_rooms[target_room_idx][room_position] = to_move
                # out.append((cost, (new_waitings, new_rooms)))
                out.append((cost, (tuple(new_waitings), tuple(map(tuple, new_rooms)))))

        return out

    # extract words
    rooms = []
    for room_col in ROOM_COLS:
        a, b = (input_lines[row][room_col] for row in [2, 3])

        rooms.append((a, b))
        # rooms.append(tuple(a+b))
    rooms = tuple(rooms)
    print(rooms)
    waitings = ("",) * len(WAITING_AREAS)

    out = dijkstra((waitings, rooms), expand, FINAL_NODE)[0][FINAL_NODE]

    if out:
        print("out:    ", out)
    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD


async def main() -> None:
    dirname = path.dirname(__file__)
    infile = path.join(dirname, "input.txt")
    with open(infile) as input_file:
        input_lines = [l for l in input_file]

    puzzle(input_lines)


if __name__ == "__main__":
    asyncio.run(main())
