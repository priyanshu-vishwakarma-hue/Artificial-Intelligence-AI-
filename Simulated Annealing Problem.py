

import math
import random
from typing import List, Tuple

def conflicts(queens: List[int]) -> int:
    clashes = 0
    size = len(queens)
    for i in range(size):
        for j in range(i + 1, size):
            if queens[i] == queens[j] or abs(queens[i] - queens[j]) == abs(i - j):
                clashes += 1
    return clashes

def print_board(queens: List[int]) -> None:
    size = len(queens)
    for r in range(1, size + 1):
        row = ["Q" if queens[c] == r else "." for c in range(size)]
        print(" ".join(row))
    print()

def neighbor(queens: List[int]) -> Tuple[List[int], str]:
    size = len(queens)
    nxt = queens[:]
    if random.random() < 0.5:
        col = random.randrange(size)
        old = nxt[col]
        new = random.choice([r for r in range(1, size + 1) if r != old])
        nxt[col] = new
        return nxt, f"Move queen in col {col+1}: {old} → {new}"
    else:
        a, b = random.sample(range(size), 2)
        nxt[a], nxt[b] = nxt[b], nxt[a]
        return nxt, f"Swap queens in col {a+1} and {b+1}"

def anneal(start: List[int], t: float = 50.0, cool: float = 0.98, stop: float = 1e-3) -> Tuple[List[int], int]:
    state = start[:]
    cost = conflicts(state)
    best_state = state[:]
    best_cost = cost
    step = 0

    print("Running annealing...\n")
    print(f"Start: {state}, Conflicts: {cost}\n")

    while t > stop and cost > 0:
        trial, act = neighbor(state)
        trial_cost = conflicts(trial)
        delta = trial_cost - cost
        ok = delta <= 0 or random.random() < math.exp(-delta / t)

        if ok:
            state = trial
            cost = trial_cost
            if cost < best_cost:
                best_state = state[:]
                best_cost = cost

        step += 1
        print(f"Step {step:3d} | Temp: {t:7.4f} | {act:30s} | Conflicts: {trial_cost:2d} | Accepted: {ok}")

        t *= cool

        if best_cost == 0:
            break

    print("\nDone.")
    print("Best board:")
    print_board(best_state)
    print(f"Conflicts left: {best_cost}")
    return best_state, best_cost

if __name__ == "__main__":
    start_board = [3, 1, 6, 8, 5, 2, 4, 7]
    anneal(start_board)


