"""Tests for shortest-path algorithms using synthetic graphs only."""

from __future__ import annotations

from math import isinf

import networkx as nx
import pytest

from redmond_graph.algorithms import a_star, dijkstra
from redmond_graph.graph_builder import build_synthetic_grid_graph


def test_dijkstra_and_astar_match_networkx_shortest_path_length() -> None:
    graph = build_synthetic_grid_graph(rows=5, cols=5, spacing_m=100.0)
    source = (0, 0)
    target = (4, 4)

    expected = nx.shortest_path_length(graph, source, target, weight="length")

    d_distance, d_path, _ = dijkstra(graph, source, target)
    a_distance, a_path, _ = a_star(graph, source, target)

    assert d_distance == pytest.approx(expected)
    assert a_distance == pytest.approx(expected)
    assert d_path[0] == source and d_path[-1] == target
    assert a_path[0] == source and a_path[-1] == target


def test_astar_explores_no_more_nodes_than_dijkstra_on_grid() -> None:
    graph = build_synthetic_grid_graph(rows=8, cols=8, spacing_m=50.0)
    source = (0, 0)
    target = (7, 7)

    _, _, d_explored = dijkstra(graph, source, target)
    _, _, a_explored = a_star(graph, source, target)

    assert a_explored <= d_explored


def test_unreachable_target_returns_infinite_distance_and_empty_path() -> None:
    graph = build_synthetic_grid_graph(rows=3, cols=3, spacing_m=100.0)
    source = (0, 0)
    target = (2, 2)

    for predecessor in list(graph.predecessors(target)):
        graph.remove_edge(predecessor, target)
    for successor in list(graph.successors(target)):
        graph.remove_edge(target, successor)

    d_distance, d_path, _ = dijkstra(graph, source, target)
    a_distance, a_path, _ = a_star(graph, source, target)

    assert isinf(d_distance)
    assert isinf(a_distance)
    assert d_path == []
    assert a_path == []
