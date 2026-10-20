"""Visualization helpers for plotting road graphs and routes."""

from __future__ import annotations

from pathlib import Path
from typing import Hashable

import matplotlib.pyplot as plt
import networkx as nx


def plot_graph_with_route(
    graph: nx.DiGraph,
    path: list[Hashable],
    output_path: Path | str,
) -> Path:
    """Plot a road graph and highlight a route, then save it as a PNG.

    The base graph is shown in light gray, while the chosen route is shown in
    red with explicit start and end points.
    """
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 10))

    for u, v in graph.edges():
        x1, y1 = graph.nodes[u]["x"], graph.nodes[u]["y"]
        x2, y2 = graph.nodes[v]["x"], graph.nodes[v]["y"]
        ax.plot([x1, x2], [y1, y2], color="lightgray", linewidth=0.7, alpha=0.8)

    if len(path) >= 2:
        route_x = [float(graph.nodes[node]["x"]) for node in path]
        route_y = [float(graph.nodes[node]["y"]) for node in path]
        ax.plot(route_x, route_y, color="red", linewidth=2.5, label="Route")
        ax.scatter(route_x[0], route_y[0], color="green", s=40, label="Start")
        ax.scatter(route_x[-1], route_y[-1], color="blue", s=40, label="End")

    ax.set_title("Redmond Road Network Route")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.legend(loc="best")
    ax.set_aspect("equal", adjustable="box")
    fig.tight_layout()
    fig.savefig(output, dpi=150)
    plt.close(fig)

    return output
