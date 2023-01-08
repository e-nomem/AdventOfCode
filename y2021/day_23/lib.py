from collections.abc import Sequence
from typing import Optional

Hallway = Sequence[Optional[str]]
Room = Sequence[Optional[str]]
Rooms = Sequence[Room]


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


def parse(input_lines: list[str]) -> tuple[Hallway, Rooms]:
    hallway = ["" for c in input_lines[1] if c == "."]
    rooms = tuple(map(tuple, zip(*(c for c in (row.strip("#").split("#") for row in input_lines[2:-1])))))

    hallway_midpoint = len(hallway) // 2
    for i in range(len(rooms) // 2):
        idx = 2 * i
        hallway[hallway_midpoint - idx - 1] = "E"
        hallway[hallway_midpoint + idx + 1] = "E"

    return tuple(hallway), rooms
