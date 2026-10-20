"""Routing algorithms implemented from scratch for learning purposes."""

from __future__ import annotations

import heapq
from math import asin, cos, radians, sin, sqrt
from typing import Hashable

import networkx as nx


def haversine_distance_meters(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    """Compute the great-circle distance between two latitude/longitude points.

    This is the straight-line distance over Earth's surface and provides an
    optimistic travel estimate for A* in road networks.
    """
    earth_radius_m = 6_371_000.0

    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return earth_radius_m * c


def _reconstruct_path(
    predecessors: dict[Hashable, Hashable],
    source: Hashable,
    target: Hashable,
) -> list[Hashable]:
    path = [target]
    current = target
    while current != source:
        current = predecessors[current]
        path.append(current)
    path.reverse()
    return path


def dijkstra(
    graph: nx.DiGraph,
    source: Hashable,
    target: Hashable,
    weight: str = "length",
) -> tuple[float, list[Hashable], int]:
    """Find the shortest path by always expanding the closest known frontier.

    Dijkstra's algorithm guarantees optimal paths for non-negative edge costs
    by settling nodes in order of increasing path cost from the source.
    """
    if source not in graph or target not in graph:
        raise ValueError("source and target must both exist in the graph")

    queue: list[tuple[float, Hashable]] = [(0.0, source)]
    distances: dict[Hashable, float] = {source: 0.0}
    predecessors: dict[Hashable, Hashable] = {}
    settled: set[Hashable] = set()
    explored = 0

    while queue:
        current_distance, node = heapq.heappop(queue)
        if node in settled:
            continue

        settled.add(node)
        explored += 1

        if node == target:
            path = _reconstruct_path(predecessors, source, target)
            return current_distance, path, explored

        for neighbor, edge_data in graph[node].items():
            if neighbor in settled:
                continue

            edge_cost = float(edge_data.get(weight, 1.0))
            new_distance = current_distance + edge_cost

            if new_distance < distances.get(neighbor, float("inf")):
                distances[neighbor] = new_distance
                predecessors[neighbor] = node
                heapq.heappush(queue, (new_distance, neighbor))

    return float("inf"), [], explored


def _a_star_heuristic(graph: nx.DiGraph, node: Hashable, target: Hashable) -> float:
    node_data = graph.nodes[node]
    target_data = graph.nodes[target]
    return haversine_distance_meters(
        lat1=float(node_data["y"]),
        lon1=float(node_data["x"]),
        lat2=float(target_data["y"]),
        lon2=float(target_data["x"]),
    )


def a_star(
    graph: nx.DiGraph,
    source: Hashable,
    target: Hashable,
    weight: str = "length",
) -> tuple[float, list[Hashable], int]:
    """Find a shortest path using Dijkstra plus a goal-directed heuristic.

    A* combines known path cost with an estimate to the target. With an
    admissible heuristic like haversine distance, it still returns optimal
    routes while often exploring fewer nodes than Dijkstra.
    """
    if source not in graph or target not in graph:
        raise ValueError("source and target must both exist in the graph")

    open_queue: list[tuple[float, float, Hashable]] = []
    start_h = _a_star_heuristic(graph, source, target)
    heapq.heappush(open_queue, (start_h, 0.0, source))

    g_scores: dict[Hashable, float] = {source: 0.0}
    predecessors: dict[Hashable, Hashable] = {}
    settled: set[Hashable] = set()
    explored = 0

    while open_queue:
        _, current_g, node = heapq.heappop(open_queue)
        if node in settled:
            continue

        settled.add(node)
        explored += 1

        if node == target:
            path = _reconstruct_path(predecessors, source, target)
            return current_g, path, explored

        for neighbor, edge_data in graph[node].items():
            if neighbor in settled:
                continue

            edge_cost = float(edge_data.get(weight, 1.0))
            tentative_g = current_g + edge_cost

            if tentative_g < g_scores.get(neighbor, float("inf")):
                g_scores[neighbor] = tentative_g
                predecessors[neighbor] = node
                f_score = tentative_g + _a_star_heuristic(graph, neighbor, target)
                heapq.heappush(open_queue, (f_score, tentative_g, neighbor))

    return float("inf"), [], explored


def bidirectional_search(
    graph: nx.DiGraph,
    source: Hashable,
    target: Hashable,
    weight: str = "length",
) -> tuple[float, list[Hashable], int]:
    """Placeholder for a future bidirectional shortest-path implementation.

    TODO: implement a forward-and-backward search that meets in the middle to
    reduce exploration on large road graphs.
    """
    raise NotImplementedError("TODO: bidirectional search is not implemented yet")
