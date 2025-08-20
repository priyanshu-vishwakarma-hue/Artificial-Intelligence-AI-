
import heapq

class HamiltonianCycleSolver:
    def __init__(self, adj_matrix):
        self.graph = adj_matrix
        self.n = len(adj_matrix)
        self.start = 0

    def find_cycle(self):
        path = [self.start]
        visited = {self.start}
        cost = 0
        est = self.estimate_cost(visited)

        pq = []
        heapq.heappush(pq, (est, cost, path, visited))

        best_path = None
        best_cost = float("inf")

        while pq:
            total_est, curr_cost, curr_path, seen = heapq.heappop(pq)
            last = curr_path[-1]

            if len(curr_path) == self.n:
                if self.graph[last][self.start] > 0:
                    cycle_cost = curr_cost + self.graph[last][self.start]
                    if cycle_cost < best_cost:
                        best_path = curr_path + [self.start]
                        best_cost = cycle_cost
                continue

            for nxt in range(self.n):
                if self.graph[last][nxt] > 0 and nxt not in seen:
                    new_path = curr_path + [nxt]
                    new_seen = seen | {nxt}
                    new_cost = curr_cost + self.graph[last][nxt]
                    new_est = new_cost + self.estimate_cost(new_seen)
                    heapq.heappush(pq, (new_est, new_cost, new_path, new_seen))

        return best_path, best_cost if best_path else (None, None)

    def estimate_cost(self, visited):
        remaining = set(range(self.n)) - visited
        if not remaining:
            return 0
        min_edge = float("inf")
        for i in range(self.n):
            for j in range(self.n):
                if i != j and self.graph[i][j] > 0:
                    min_edge = min(min_edge, self.graph[i][j])
        return len(remaining) * (min_edge if min_edge != float("inf") else 1)


def build_matrix(n, edges):
    mat = [[0] * n for _ in range(n)]
    for u, v, w in edges:
        mat[u-1][v-1] = w
        mat[v-1][u-1] = w
    return mat


def main():
    n = 5
    edges = [
        (1, 2, 14),
        (2, 3, 38),
        (3, 4, 9),
        (4, 5, 22),
        (5, 1, 16),
        (1, 3, 22),
        (2, 5, 17),
        (2, 4, 24)
    ]

    mat = build_matrix(n, edges)
    solver = HamiltonianCycleSolver(mat)
    cycle, cost = solver.find_cycle()

    if cycle:
        print("Hamiltonian cycle with minimum cost:")
        print(" -> ".join(str(v + 1) for v in cycle))
        print("Total cost:", cost)
    else:
        print("No Hamiltonian cycle exists.")


if __name__ == "__main__":
    main()
