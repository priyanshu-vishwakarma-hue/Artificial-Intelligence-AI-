
import heapq
from typing import Tuple, List, Dict, Optional
import math

State = Tuple[int, ...]

GOAL: State = (1,2,3,4,5,6,7,8,0)


def is_solvable(state: State) -> bool:
    arr = [x for x in state if x != 0]
    inv = 0
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] > arr[j]:
                inv += 1
    return inv % 2 == 0


def manhattan(state: State, goal: State = GOAL) -> int:
    distance = 0
    for i, tile in enumerate(state):
        if tile == 0:
            continue
        # current coordinates
        r1, c1 = divmod(i, 3)
        # goal coordinates for tile (tile -1)
        goal_index = goal.index(tile)
        r2, c2 = divmod(goal_index, 3)
        distance += abs(r1 - r2) + abs(c1 - c2)
    return distance


def neighbors(state: State) -> List[Tuple[State, str]]:
    results = []
    zero_idx = state.index(0)
    r, c = divmod(zero_idx, 3)
    moves = []
    if r > 0: moves.append((-1, 0, "Up"))
    if r < 2: moves.append((1, 0, "Down"))
    if c > 0: moves.append((0, -1, "Left"))
    if c < 2: moves.append((0, 1, "Right"))

    for dr, dc, name in moves:
        nr, nc = r + dr, c + dc
        swap_idx = nr * 3 + nc
        new_state = list(state)
        new_state[zero_idx], new_state[swap_idx] = new_state[swap_idx], new_state[zero_idx]
        results.append((tuple(new_state), name))
    return results


def reconstruct_path(came_from: Dict[State, Tuple[Optional[State], Optional[str]]],
                     current: State) -> List[str]:
    path = []
    while came_from[current][0] is not None:
        prev, move = came_from[current]
        path.append(move)
        current = prev
    path.reverse()
    return path


def a_star(start: State, goal: State = GOAL):
    if start == goal:
        return [], 0, 0

    if not is_solvable(start):
        raise ValueError("This puzzle configuration is not solvable.")

    open_heap = []
    g_score: Dict[State, int] = {start: 0}
    f_score = manhattan(start, goal)
    heapq.heappush(open_heap, (f_score, 0, start))
    came_from: Dict[State, Tuple[Optional[State], Optional[str]]] = {start: (None, None)}
    closed_set = set()

    nodes_expanded = 0
    tie = 1
    max_queue_size = 1

    while open_heap:
        current_f, _, current = heapq.heappop(open_heap)

        if current in closed_set:
            continue

        if current == goal:
            moves = reconstruct_path(came_from, current)
            return moves, nodes_expanded, max_queue_size

        closed_set.add(current)
        nodes_expanded += 1

        for nbr, move in neighbors(current):
            if nbr in closed_set:
                continue
            tentative_g = g_score[current] + 1

            if tentative_g < g_score.get(nbr, math.inf):
                came_from[nbr] = (current, move)
                g_score[nbr] = tentative_g
                f = tentative_g + manhattan(nbr, goal)
                tie += 1
                heapq.heappush(open_heap, (f, tie, nbr))
                max_queue_size = max(max_queue_size, len(open_heap))

    raise RuntimeError("A* failed to find a solution (shouldn't happen for solvable puzzles).")


def pretty_print(state: State):
    for i in range(0, 9, 3):
        row = state[i:i+3]
        print(' '.join(str(x) if x != 0 else '_' for x in row))
    print()


if __name__ == "__main__":
    start_state = (1,2,3,0,6,7,4,5,8)

    print("Start state:")
    pretty_print(start_state)
    print("Goal state:")
    pretty_print(GOAL)

    try:
        moves, nodes_expanded, max_q = a_star(start_state)
        print(f"Solution found in {len(moves)} moves.")
        print("Moves sequence (blank's movement):", moves)
        print(f"Nodes expanded: {nodes_expanded}, max queue size: {max_q}\n")

        cur = start_state
        for i, m in enumerate(moves, 1):
            for nbr, mv in neighbors(cur):
                if mv == m:
                    cur = nbr
                    break
            print(f"After move {i}: {m}")
            pretty_print(cur)

    except ValueError as e:
        print(e)
