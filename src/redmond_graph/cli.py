"""Command-line interface for running routing experiments."""

from __future__ import annotations

import argparse
from pathlib import Path

from redmond_graph.algorithms import a_star, dijkstra
from redmond_graph.graph_builder import build_redmond_drive_graph, nearest_node_by_latlon
from redmond_graph.viz import plot_graph_with_route


def parse_latlon(value: str) -> tuple[float, float]:
    """Parse `lat,lon` text into a coordinate tuple."""
    try:
        lat_text, lon_text = value.split(",", maxsplit=1)
        return float(lat_text.strip()), float(lon_text.strip())
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Coordinates must be in the format 'lat,lon'") from exc


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI parser with the `route` subcommand."""
    parser = argparse.ArgumentParser(prog="redmond-route")
    subparsers = parser.add_subparsers(dest="command", required=True)

    route = subparsers.add_parser(
        "route",
        help="Find and compare Dijkstra and A* routes between two coordinates",
    )
    route.add_argument(
        "--origin",
        type=parse_latlon,
        default=(47.6423, -122.1391),
        help="Origin coordinate as lat,lon (default: Microsoft Redmond campus area)",
    )
    route.add_argument(
        "--destination",
        type=parse_latlon,
        default=(47.6617, -122.1210),
        help="Destination coordinate as lat,lon (default: Marymoor Park)",
    )
    route.add_argument(
        "--output",
        type=Path,
        default=Path("data/route.png"),
        help="Output PNG path for the plotted route",
    )

    return parser


def run_route_command(
    origin: tuple[float, float],
    destination: tuple[float, float],
    output: Path,
) -> int:
    """Run routing algorithms on the Redmond graph and save a route image."""
    graph = build_redmond_drive_graph()

    origin_node = nearest_node_by_latlon(graph, latitude=origin[0], longitude=origin[1])
    destination_node = nearest_node_by_latlon(
        graph,
        latitude=destination[0],
        longitude=destination[1],
    )

    d_distance, d_path, d_explored = dijkstra(graph, origin_node, destination_node)
    a_distance, a_path, a_explored = a_star(graph, origin_node, destination_node)

    print(f"Dijkstra: distance={d_distance:.2f} m, explored={d_explored}")
    print(f"A*:       distance={a_distance:.2f} m, explored={a_explored}")

    if a_path:
        image_path = plot_graph_with_route(graph, a_path, output)
        print(f"Saved route map to {image_path}")
    elif d_path:
        image_path = plot_graph_with_route(graph, d_path, output)
        print(f"Saved route map to {image_path}")
    else:
        print("No route found between the selected points.")

    return 0


def main() -> int:
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "route":
        return run_route_command(args.origin, args.destination, args.output)

    parser.error("Unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
