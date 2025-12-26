import heapq


def dijkstra(graph: dict, start):
    """
    graph: {vertex: [(neighbor, weight), ...], ...}
    start: початкова вершина
    return: (dist, prev)
      dist[v] - найкоротша відстань від start до v
      prev[v] - попередня вершина на найкоротшому шляху
    """
    dist = {v: float("inf") for v in graph}
    prev = {v: None for v in graph}

    dist[start] = 0
    heap = [(0, start)]

    while heap:
        cur_dist, v = heapq.heappop(heap)

        if cur_dist != dist[v]:
            continue

        for to, w in graph[v]:
            new_dist = cur_dist + w
            if new_dist < dist[to]:
                dist[to] = new_dist
                prev[to] = v
                heapq.heappush(heap, (new_dist, to))

    return dist, prev


def build_path(prev: dict, start, target):
    """Відновлення шляху start -> target через prev."""
    if start == target:
        return [start]
    if prev[target] is None:
        return []

    path = []
    v = target
    while v is not None:
        path.append(v)
        if v == start:
            break
        v = prev[v]

    if path[-1] != start:
        return []
    path.reverse()
    return path


if __name__ == "__main__":
    # Приклад графа (зважений, орієнтований)
    graph = {
        "A": [("B", 4), ("C", 2)],
        "B": [("C", 5), ("D", 10)],
        "C": [("E", 3)],
        "D": [("F", 11)],
        "E": [("D", 4)],
        "F": [],
    }

    start_vertex = "A"
    dist, prev = dijkstra(graph, start_vertex)

    print(f"Початкова вершина: {start_vertex}\n")
    print("Найкоротші відстані до всіх вершин:")
    for v in graph:
        print(f"  {start_vertex} -> {v}: {dist[v]}")

    print("\nПриклади відновлення шляхів:")
    for target in graph:
        path = build_path(prev, start_vertex, target)
        if path:
            print(f"  Шлях до {target}: {' -> '.join(path)} (довжина {dist[target]})")
        else:
            print(f"  Шлях до {target}: немає")
