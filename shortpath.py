"""
Using Floyd's Algorithm:
(a) Find the shortest paths between all pairs of vertices.
(b) Determine the eccentricity of vertices, the radius, and diameter of the graph.
(c) Identify central and peripheral vertices.

Using Dijkstra's Algorithm:
Find shortest paths from vertex 4 to all other vertices.

Using the Bellman-Ford Algorithm:
Find shortest paths from vertex 4 to all other vertices.

Using the Bellman-Kalaba Algorithm:
Find shortest paths to vertex 4 from all other vertices.
"""

import networkx as nx
import matplotlib.pyplot as plt


# Function to read the graph from a file
def read_graph_from_file(file_path):
    G = nx.Graph()
    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3:
                u, v, w = map(int, parts)
                G.add_edge(u, v, weight=w)
            else:
                raise ValueError("Line format should be: vertex1 vertex2 weight")
    return G


def calculate_shortest_paths_to(graph, target):
    # Initialize a graph to store reversed edges with same weights
    reversed_graph = nx.Graph()
    for u, v, data in graph.edges(data=True):
        weight = data["weight"]
        reversed_graph.add_edge(v, u, weight=weight)  # Reverse the edge direction

    # Calculate shortest paths from all nodes to the 'target' by running
    # Bellman-Ford on the reversed graph from 'target'
    distances = nx.single_source_bellman_ford_path_length(reversed_graph, target)
    return distances


# Read the graph
file_path = "data/graph_7.txt"
G = read_graph_from_file(file_path)

# edges = [(1, 2, 3), (2, 3, 4), (1, 3, 7), (3, 4, 2), (4, 2, 5), (1, 4, 1), (4, 1, 6)]
# G.add_weighted_edges_from(edges)

# Plot the graph
pos = nx.spring_layout(G)
nx.draw(
    G,
    pos,
    with_labels=True,
    node_color="skyblue",
    node_size=700,
    edge_color="k",
    font_size=15,
    font_color="darkred",
)
edge_labels = dict(
    [
        (
            (
                u,
                v,
            ),
            d["weight"],
        )
        for u, v, d in G.edges(data=True)
    ]
)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.savefig("graph.png")

lengths = dict(nx.all_pairs_bellman_ford_path_length(G))

# Compute eccentricities, radius, and diameter
eccentricities = nx.eccentricity(G, sp=lengths)
radius = nx.radius(G, e=eccentricities)
diameter = nx.diameter(G, e=eccentricities)
center = nx.center(G, e=eccentricities)
periphery = nx.periphery(G, e=eccentricities)

print("Shortest paths between all pairs using Floyd:", lengths)
print("Eccentricities:", eccentricities)
print("Radius:", radius)
print("Diameter:", diameter)
print("Center:", center)
print("Periphery:", periphery)

paths_from_4 = nx.single_source_dijkstra_path_length(G, 4)
print("Shortest paths from vertex 4 using Djikstra:", paths_from_4)

paths_from_4_bf = nx.single_source_bellman_ford_path_length(G, 4)
print("Shortest paths from vertex 4 using Bellman-Ford:", paths_from_4_bf)

# Calculate shortest paths to vertex 4 from all other vertices
target_vertex = 4
distances_to_target = calculate_shortest_paths_to(G, target_vertex)
print(
    f"Shortest paths to vertex {target_vertex} using Bellman-Kalaba:",
    distances_to_target,
)
