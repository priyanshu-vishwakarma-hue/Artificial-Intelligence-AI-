
import networkx as nx
import matplotlib.pyplot as plt
import time

def end_state(position):
    return all(x == 0 for x in position)

def generate_moves(position):
    actions = []
    for i, pile in enumerate(position):
        for take in range(1, pile + 1):
            nxt = list(position)
            nxt[i] -= take
            actions.append((position, tuple(nxt)))
    return actions

def pure_minimax(position, maximize=True, g=None, parent=None, route=None):
    g = g or nx.DiGraph()
    route = route or {}
    node = str(position)
    if parent: g.add_edge(str(parent), node)
    if end_state(position):
        val = -1 if maximize else 1
        g.nodes[node]["label"] = f"{position}\nVal={val}"
        return val, g, route
    score = float('-inf') if maximize else float('inf')
    chosen = None
    for _, nxt in generate_moves(position):
        res, g, route = pure_minimax(nxt, not maximize, g, position, route)
        if maximize and res > score or not maximize and res < score:
            score, chosen = res, nxt
    g.nodes[node]["label"] = f"{position}\n{'MAX' if maximize else 'MIN'}={score}"
    if chosen: route[position] = chosen
    return score, g, route

def pruned_minimax(position, a=float('-inf'), b=float('inf'), maximize=True, g=None, parent=None, route=None):
    g = g or nx.DiGraph()
    route = route or {}
    node = str(position)
    if parent: g.add_edge(str(parent), node)
    if end_state(position):
        val = -1 if maximize else 1
        g.nodes[node]["label"] = f"{position}\nVal={val}"
        return val, g, route
    score = float('-inf') if maximize else float('inf')
    chosen = None
    for _, nxt in generate_moves(position):
        res, g, route = pruned_minimax(nxt, a, b, not maximize, g, position, route)
        if maximize:
            if res > score: score, chosen = res, nxt
            a = max(a, score)
        else:
            if res < score: score, chosen = res, nxt
            b = min(b, score)
        if b <= a: break
    g.nodes[node]["label"] = f"{position}\n{'MAX' if maximize else 'MIN'}={score}"
    if chosen: route[position] = chosen
    return score, g, route

def visualize(g, route, start_pos, title):
    layout = nx.spring_layout(g, seed=42)
    labels = nx.get_node_attributes(g, "label")
    edges_on_path = []
    cur = start_pos
    while cur in route:
        nxt = route[cur]
        edges_on_path.append((str(cur), str(nxt)))
        cur = nxt
    plt.figure(figsize=(12, 8))
    nx.draw(g, layout, with_labels=False, node_size=1800, node_color="lavender")
    nx.draw_networkx_labels(g, layout, labels, font_size=8)
    nx.draw_networkx_edges(g, layout, edgelist=edges_on_path, edge_color="crimson", width=2)
    plt.title(title)
    plt.show()

init = (1, 2, 3)
t0 = time.time()
val_minimax, g1, path1 = pure_minimax(init)
elapsed1 = time.time() - t0
t1 = time.time()
val_ab, g2, path2 = pruned_minimax(init)
elapsed2 = time.time() - t1

visualize(g1, path1, init, f"Tree (Minimax) Nodes={len(g1.nodes)}")
visualize(g2, path2, init, f"Tree (Alpha-Beta) Nodes={len(g2.nodes)}")

print("\n--- Results ---")
print(f"Start: {init}")
print(f"Minimax -> Value={val_minimax}, Nodes={len(g1.nodes)}, Time={elapsed1:.6f}s")
print(f"Alpha-Beta -> Value={val_ab}, Nodes={len(g2.nodes)}, Time={elapsed2:.6f}s")
print(f"Best route (Alpha-Beta): {path2}")
