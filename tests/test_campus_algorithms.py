
import unittest

from src.campus_algorithms import (
    bfs_shortest_paths,
    reconstruct_path,
    dfs_traversal,
    dfs_path,
    dijkstra,
    rebuild_path,
    prim,
)


class TestCampusAlgorithms(unittest.TestCase):

    def setUp(self):
        """Create sample graphs before each test."""

        # Unweighted, undirected graph
        self.unweighted_graph = {
            "A": {"B", "C"},
            "B": {"A", "D"},
            "C": {"A", "D"},
            "D": {"B", "C"},
            "E": set(),  # Isolated node
        }

        # Weighted, undirected graph
        self.weighted_graph = {
            "A": [("B", 2), ("C", 5)],
            "B": [("A", 2), ("C", 1), ("D", 4)],
            "C": [("A", 5), ("B", 1), ("D", 2)],
            "D": [("B", 4), ("C", 2)],
            "E": [],  # Isolated node
        }

    # --------------------------------------------------
    # BFS TESTS
    # --------------------------------------------------

    def test_bfs_shortest_path(self):
        dist, parent, order = bfs_shortest_paths(
            self.unweighted_graph, "A"
        )

        path = reconstruct_path(parent, "A", "D")

        self.assertEqual(dist["D"], 2)
        self.assertEqual(path, ["A", "B", "D"])
        self.assertEqual(order[0], "A")

    def test_bfs_unreachable_node(self):
        dist, parent, _ = bfs_shortest_paths(
            self.unweighted_graph, "A"
        )

        self.assertNotIn("E", dist)
        self.assertEqual(
            reconstruct_path(parent, "A", "E"), []
        )

    # --------------------------------------------------
    # DFS TESTS
    # --------------------------------------------------

    def test_dfs_traversal(self):
        order = dfs_traversal(self.unweighted_graph, "A")

        self.assertEqual(order[0], "A")
        self.assertEqual(set(order), {"A", "B", "C", "D"})
        self.assertEqual(len(order), 4)

    def test_dfs_valid_path(self):
        path = dfs_path(self.unweighted_graph, "A", "D")

        self.assertTrue(path)
        self.assertEqual(path[0], "A")
        self.assertEqual(path[-1], "D")

        # Verify that every step follows an actual edge
        for u, v in zip(path, path[1:]):
            self.assertIn(v, self.unweighted_graph[u])

    def test_dfs_unreachable_node(self):
        path = dfs_path(self.unweighted_graph, "A", "E")
        self.assertEqual(path, [])

    # --------------------------------------------------
    # DIJKSTRA TESTS
    # --------------------------------------------------

    def test_dijkstra_shortest_distance(self):
        dist, parent = dijkstra(self.weighted_graph, "A")

        self.assertEqual(dist["D"], 5)
        self.assertEqual(
            rebuild_path(parent, "D"),
            ["A", "B", "C", "D"]
        )

    def test_dijkstra_unreachable_node(self):
        dist, parent = dijkstra(self.weighted_graph, "A")

        self.assertNotIn("E", dist)
        self.assertEqual(rebuild_path(parent, "E"), [])

    # --------------------------------------------------
    # PRIM TESTS
    # --------------------------------------------------

    def test_prim_total_cost(self):
        edges, cost = prim(self.weighted_graph, "A")

        # Expected MST: A-B (2), B-C (1), C-D (2)
        self.assertEqual(cost, 5)
        self.assertEqual(len(edges), 3)

    def test_prim_no_cycles(self):
        edges, _ = prim(self.weighted_graph, "A")

        # Union-Find: an edge creates a cycle if its
        # endpoints already belong to the same component.
        parent = {}

        def find(node):
            parent.setdefault(node, node)
            if parent[node] != node:
                parent[node] = find(parent[node])
            return parent[node]

        for u, v, _ in edges:
            root_u = find(u)
            root_v = find(v)

            self.assertNotEqual(
                root_u, root_v,
                "Prim's algorithm produced a cycle."
            )

            parent[root_u] = root_v


if __name__ == "__main__":
    unittest.main()
