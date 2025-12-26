import uuid
from collections import deque

import matplotlib.pyplot as plt
import networkx as nx


class Node:
    def __init__(self, key, color="#D9D9D9"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def hex_to_rgb(hex_color: str):
    hex_color = hex_color.lstrip("#")
    return int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)


def rgb_to_hex(rgb):
    r, g, b = rgb
    return f"#{r:02X}{g:02X}{b:02X}"


def make_gradient(n: int, start="#1A2A6C", end="#C4E0FF"):
    """n кольорів від start (темніший) до end (світліший)"""
    if n <= 0:
        return []
    if n == 1:
        return [start]

    s = hex_to_rgb(start)
    e = hex_to_rgb(end)

    colors = []
    for i in range(n):
        t = i / (n - 1)
        r = round(s[0] + (e[0] - s[0]) * t)
        g = round(s[1] + (e[1] - s[1]) * t)
        b = round(s[2] + (e[2] - s[2]) * t)
        colors.append(rgb_to_hex((r, g, b)))
    return colors


def collect_nodes_iterative(root: Node):
    """Збираємо всі вузли дерева без рекурсії."""
    if root is None:
        return []
    nodes = []
    stack = [root]
    seen = set()
    while stack:
        node = stack.pop()
        if node is None or node.id in seen:
            continue
        seen.add(node.id)
        nodes.append(node)
        
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return nodes


def build_graph_iterative(root: Node):
    """
    Будуємо networkx DiGraph + позиції вузлів
    """
    tree = nx.DiGraph()
    pos = {root.id: (0.0, 0.0)}

    stack = [(root, 0.0, 0.0, 1)]
    while stack:
        node, x, y, layer = stack.pop()
        tree.add_node(node.id, color=node.color, label=node.val)

        if node.left:
            tree.add_edge(node.id, node.left.id)
            lx = x - 1 / (2 ** layer)
            ly = y - 1
            pos[node.left.id] = (lx, ly)
            stack.append((node.left, lx, ly, layer + 1))

        if node.right:
            tree.add_edge(node.id, node.right.id)
            rx = x + 1 / (2 ** layer)
            ry = y - 1
            pos[node.right.id] = (rx, ry)
            stack.append((node.right, rx, ry, layer + 1))

    return tree, pos


def draw_tree(root: Node, title: str):
    tree, pos = build_graph_iterative(root)
    colors = [node[1]["color"] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]["label"] for node in tree.nodes(data=True)}

    plt.clf()
    plt.title(title)
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
    plt.axis("off")


def dfs_iterative(root: Node):
    """DFS (preorder) ітератвно через стек"""
    if root is None:
        return []
    order = []
    stack = [root]
    seen = set()
    while stack:
        node = stack.pop()
        if node is None or node.id in seen:
            continue
        seen.add(node.id)
        order.append(node)

        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return order


def bfs_iterative(root: Node):
    """BFS ітеративно через чергу"""
    if root is None:
        return []
    order = []
    q = deque([root])
    seen = set([root.id])
    while q:
        node = q.popleft()
        order.append(node)

        if node.left and node.left.id not in seen:
            seen.add(node.left.id)
            q.append(node.left)
        if node.right and node.right.id not in seen:
            seen.add(node.right.id)
            q.append(node.right)
    return order


def reset_colors(root: Node, color="#D9D9D9"):
    for n in collect_nodes_iterative(root):
        n.color = color


def visualize_traversal(root: Node, mode: str = "DFS", pause_sec: float = 0.7):
    mode = mode.upper().strip()
    if mode not in ("DFS", "BFS"):
        raise ValueError("mode має бути 'DFS' або 'BFS'")

    order = dfs_iterative(root) if mode == "DFS" else bfs_iterative(root)
    gradient = make_gradient(len(order), start="#1A2A6C", end="#C4E0FF")

    print(f"\nРежим обходу: {mode}")
    print("Порядок відвідування вузлів:", " -> ".join(str(n.val) for n in order))

    plt.figure(figsize=(8, 5))

    for i, node in enumerate(order):
        node.color = gradient[i]
        title = f"{mode}: крок {i+1}/{len(order)} (відвідали вузол {node.val})"
        draw_tree(root, title=title)
        plt.pause(pause_sec)

    plt.show()


if __name__ == "__main__":
    root = Node(0)
    root.left = Node(4)
    root.left.left = Node(5)
    root.left.right = Node(10)
    root.right = Node(1)
    root.right.left = Node(3)

    reset_colors(root)
    visualize_traversal(root, mode="DFS", pause_sec=0.7)

    reset_colors(root)
    visualize_traversal(root, mode="BFS", pause_sec=0.7)
