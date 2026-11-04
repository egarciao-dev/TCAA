# campus_algorithms.py
# All graph algorithms used by the Campus Navigator.

from collections import deque
import heapq


# =========================
#  BFS (fewest hops)
# =========================

def bfs_shortest_paths(graph, start):
    """
    graph: dict[node] -> iterable of neighbors (unweighted, undirected)
    Returns:
      dist:   dict[node] -> distance in hops
      parent: dict[node] -> predecessor in BFS tree
      order:  list[node] -> BFS visit order
    """
    dist = {start: 0}
    parent = {start: None}
    order = []

    q = deque([start])

    while q:
        u = q.popleft()
        order.append(u)

        for v in sorted(graph.get(u, [])):
            if v not in dist:
                dist[v] = dist[u] + 1
                parent[v] = u
                q.append(v)

    return dist, parent, order


def reconstruct_path(parent, start, end):
    """
    Reconstruct path from start to end using parent dict.
    Returns [] if end is unreachable or not in parent.
    """
    if end not in parent:
        return []

    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = parent.get(cur)

    path.reverse()
    return path if path and path[0] == start else []


# =========================
#  DFS (traversal + any path)
# =========================

def dfs_traversal(graph, start):
    """
    Simple iterative DFS traversal.
    Returns a list with visit order.
    """
    visited_order = []
    stack = [start]
    seen = set()

    while stack:
        u = stack.pop()
        if u in seen:
            continue

        seen.add(u)
        visited_order.append(u)

        neighbors = list(graph.get(u, []))
        neighbors.sort(reverse=True)  # for deterministic order
        for v in neighbors:
            if v not in seen:
                stack.append(v)

    return visited_order


def dfs_path(graph, start, end):
    """
    DFS-based path finder.
    Returns ANY path from start to end 
    """
    if start not in graph or end not in graph:
        return []

    visited = set()
    path = []

    def dfs(u):
        if u in visited:
            return False
        visited.add(u)
        path.append(u)

        if u == end:
            return True

        for v in sorted(graph.get(u, [])):
            if dfs(v):
                return True

        # backtrack
        path.pop()
        return False

    found = dfs(start)
    return path if found else []


# =========================
#  Dijkstra (weighted shortest path)
# =========================

def dijkstra(graph, start):
    """
    graph: dict[node] -> list of (neighbor, weight)
    Returns:
      dist:   dict[node] -> minimum distance from start
      parent: dict[node] -> predecessor on shortest path
    """
    dist = {start: 0.0}
    parent = {start: None}
    pq = [(0.0, start)]  # (dist, node)

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, float("inf")):
            continue

        for v, w in graph.get(u, []):
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                parent[v] = u
                heapq.heappush(pq, (nd, v))

    return dist, parent


def rebuild_path(parent, end):
    """
    Rebuild path from parent dict (assuming start has parent None).
    """
    if end not in parent:
        return []

    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = parent.get(cur)

    path.reverse()
    return path


# =========================
#  Prim (MST)
# =========================

def prim(graph, start):
    """
    Prim's algorithm for MST on a weighted, UNDIRECTED graph:
      graph: dict[node] -> list of (neighbor, weight)

    Returns:
      mst_edges: list of (u, v, w)
      total_cost: float
    """
    visited = set([start])
    edges = []
    total_cost = 0.0

    pq = []
    for v, w in graph.get(start, []):
        heapq.heappush(pq, (w, start, v))

    while pq:
        w, u, v = heapq.heappop(pq)
        if v in visited:
            continue

        visited.add(v)
        edges.append((u, v, w))
        total_cost += w

        for nv, nw in graph.get(v, []):
            if nv not in visited:
                heapq.heappush(pq, (nw, v, nv))

    return edges, total_cost
