"""Build and transform road-network graphs for routing experiments.

This module keeps two workflows: loading real OpenStreetMap data for Redmond,
and constructing a tiny synthetic graph for tests and algorithm practice.
"""

from __future__ import annotations

from math import cos, radians
from pathlib import Path
from typing import Hashable

import networkx as nx

DEFAULT_PLACE = "Redmond, Washington, USA"
DEFAULT_GRAPHML_NAME = "redmond_drive.graphml"


def download_redmond_drive_multidigraph(place: str = DEFAULT_PLACE) -> nx.MultiDiGraph:
    """Download Redmond's drivable road network from OpenStreetMap.

    The returned graph is a `MultiDiGraph`, which preserves parallel road
    segments and directionality exactly as they appear in OSM.
    """
    import osmnx as ox

    return ox.graph_from_place(place, network_type="drive")


def load_or_download_redmond_graphml(path: Path) -> nx.MultiDiGraph:
    """Load a cached GraphML road network if available, otherwise download it.

    Caching avoids repeated network calls and gives deterministic input while
    you practice algorithms.
    """
    import osmnx as ox

    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return ox.load_graphml(path)

    graph = download_redmond_drive_multidigraph()
    ox.save_graphml(graph, path)
    return graph


def to_simple_digraph(graph: nx.MultiDiGraph) -> nx.DiGraph:
    """Convert a MultiDiGraph into a simple weighted `DiGraph`.

    For each directed node pair `(u, v)`, the shortest parallel edge by
    `length` is kept. Nodes preserve only `x` and `y` coordinates so algorithms
    and plotting remain focused on routing logic.
    """
    simple = nx.DiGraph()

    for node, data in graph.nodes(data=True):
        simple.add_node(node, x=float(data["x"]), y=float(data["y"]))

    for u, v, edge_data in graph.edges(data=True):
        length = float(edge_data.get("length", 1.0))
        if simple.has_edge(u, v):
            if length < float(simple[u][v]["length"]):
                simple[u][v]["length"] = length
        else:
            simple.add_edge(u, v, length=length)

    return simple


def build_redmond_drive_graph(data_dir: Path | str = "data") -> nx.DiGraph:
    """Build a simple directed road graph for Redmond, caching GraphML in `data/`."""
    data_path = Path(data_dir)
    graphml_path = data_path / DEFAULT_GRAPHML_NAME
    multi = load_or_download_redmond_graphml(graphml_path)
    return to_simple_digraph(multi)


def build_synthetic_grid_graph(
    rows: int = 5,
    cols: int = 5,
    spacing_m: float = 100.0,
    origin_lat: float = 47.6423,
    origin_lon: float = -122.1391,
) -> nx.DiGraph:
    """Build a small directed grid graph for tests and learning.

    Every node has `(x, y)` as `(lon, lat)`. Each neighboring pair has
    two directed edges with a `length` in meters. This mirrors the key
    attributes needed by the routing algorithms without network access.
    """
    if rows < 1 or cols < 1:
        raise ValueError("rows and cols must be >= 1")

    graph = nx.DiGraph()
    meters_to_lat = 1.0 / 111_320.0
    meters_to_lon = 1.0 / (111_320.0 * cos(radians(origin_lat)))

    for row in range(rows):
        for col in range(cols):
            lat = origin_lat + row * spacing_m * meters_to_lat
            lon = origin_lon + col * spacing_m * meters_to_lon
            graph.add_node((row, col), x=lon, y=lat)

    for row in range(rows):
        for col in range(cols):
            node = (row, col)
            if row + 1 < rows:
                down = (row + 1, col)
                graph.add_edge(node, down, length=spacing_m)
                graph.add_edge(down, node, length=spacing_m)
            if col + 1 < cols:
                right = (row, col + 1)
                graph.add_edge(node, right, length=spacing_m)
                graph.add_edge(right, node, length=spacing_m)

    return graph


def nearest_node_by_latlon(graph: nx.DiGraph, latitude: float, longitude: float) -> Hashable:
    """Return the graph node closest to a latitude/longitude point.

    This helper uses straight-line distance in coordinate space and avoids any
    dependency on external nearest-node utilities.
    """
    if not graph.nodes:
        raise ValueError("graph is empty")

    best_node: Hashable | None = None
    best_distance = float("inf")

    for node, data in graph.nodes(data=True):
        dx = float(data["x"]) - longitude
        dy = float(data["y"]) - latitude
        distance_sq = dx * dx + dy * dy
        if distance_sq < best_distance:
            best_distance = distance_sq
            best_node = node

    assert best_node is not None
    return best_node
