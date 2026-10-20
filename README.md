# redmond-road-graph

A learning project for modeling and routing algorithms using the real OpenStreetMap road network of Redmond, Washington.

## Setup

- Python 3.11
- `src/` layout package: `src/redmond_graph/`
- Tooling:
  - Ruff (formatting + linting)
  - Pytest (tests)

### Install

```bash
python -m pip install -e .[dev]
```

## Quick start

Run route comparison with default points near Microsoft Redmond campus and Marymoor Park:

```bash
redmond-route route
```

Custom coordinates:

```bash
redmond-route route --origin 47.6423,-122.1391 --destination 47.6617,-122.1210 --output data/route.png
```

The command prints distance and explored-node counts for Dijkstra and A*, then writes a PNG route map.

## Project structure

- `src/redmond_graph/graph_builder.py`: OSM download + GraphML cache + conversion to simple `DiGraph` + synthetic grid graph builder.
- `src/redmond_graph/algorithms.py`: From-scratch Dijkstra and A* (plus documented bidirectional TODO stub).
- `src/redmond_graph/viz.py`: Graph and route plotting to PNG.
- `src/redmond_graph/cli.py`: `route` command for algorithm comparison.
- `tests/`: Synthetic-graph algorithm tests only (no network access).
- `docs/learning-path.md`: Six-step learning roadmap.
- `.github/workflows/ci.yml`: CI running Ruff and Pytest.

## Assumptions

- The simple routing graph keeps only node coordinates (`x`, `y`) and edge distance (`length`) to keep teaching examples focused.
- Parallel OSM edges between the same directed node pair are reduced to the shortest `length` edge.
- Synthetic test graphs use evenly spaced bidirectional grid edges with metric lengths.
- Unreachable destinations return `(inf, [], explored_count)`.

## Development

```bash
ruff format .
ruff check .
pytest
```

## License

MIT
