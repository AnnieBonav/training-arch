# Learning Path

## Step 1: Shortest paths and practical edge costs
- **Goal:** Understand Dijkstra and A* on real road graphs and verify shortest-route correctness.
- **Key concept:** Path cost design; first use distance, then switch to travel time (`length / speed_limit`) to model realistic routing.
- **Exercise:** Add travel-time weights on edges and compare how route choices change relative to pure distance.

## Step 2: Faster search on larger maps
- **Goal:** Scale shortest-path queries to bigger regions without losing correctness.
- **Key concept:** Bidirectional search and contraction hierarchies reduce explored nodes and query latency.
- **Exercise:** Implement bidirectional Dijkstra and measure explored-node reduction versus single-direction Dijkstra.

## Step 3: Map matching noisy GPS traces
- **Goal:** Snap noisy location streams onto likely road segments.
- **Key concept:** Hidden Markov Models combine emission likelihoods (GPS noise) and transition likelihoods (graph movement).
- **Exercise:** Build a small HMM map matcher for a short synthetic GPS trace and visualize matched edges.

## Step 4: Vehicle tracking over time
- **Goal:** Estimate smoother vehicle state than raw GPS alone.
- **Key concept:** Kalman filters fuse predictions and observations for robust tracking on a road graph.
- **Exercise:** Simulate noisy motion along a path and compare raw vs filtered trajectories.

## Step 5: Rich planning and infrastructure awareness
- **Goal:** Move beyond shortest paths to operationally useful planning.
- **Key concept:** Lane-aware and cost-aware planning with additional penalties/constraints, plus V2X roadside unit coverage analysis over graph nodes/edges.
- **Exercise:** Add a coverage score for RSU-equipped segments and optimize for distance plus communication coverage.

## Step 6: 3D spatial context
- **Goal:** Extend routing and perception experiments into elevation-aware environments.
- **Key concept:** Elevation rasters and building footprints enrich graph analysis for slope and urban canyon effects.
- **Exercise:** Annotate edges with elevation change and evaluate how slope-aware costs alter selected routes.
