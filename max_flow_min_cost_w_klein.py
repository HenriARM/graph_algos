import networkx as nx
import matplotlib.pyplot as plt


def find_augmenting_path(G, source, sink, residual_capacity):
    """Find a shortest path considering only edges with residual capacity"""
    for path in nx.all_simple_paths(G, source, sink):
        # Check if the path can be used for augmentation
        if all(
            G[u][v]["capacity"] - residual_capacity.get((u, v), 0) > 0
            for u, v in zip(path[:-1], path[1:])
        ):
            return path
    return None


def augment_flow(G, path, residual_capacity):
    """Augment flow along a path and update residual capacities"""
    flow = min(
        G[u][v]["capacity"] - residual_capacity.get((u, v), 0)
        for u, v in zip(path[:-1], path[1:])
    )
    for u, v in zip(path[:-1], path[1:]):
        if (u, v) in residual_capacity:
            residual_capacity[(u, v)] += flow
        else:
            residual_capacity[(u, v)] = flow
    return flow


def simple_flow_algorithm(G, source, sink):
    """A simple flow augmentation algorithm"""
    residual_capacity = {}
    total_flow = 0

    while True:
        path = find_augmenting_path(G, source, sink, residual_capacity)
        if not path:
            break  # No augmenting path
        flow = augment_flow(G, path, residual_capacity)
        total_flow += flow

    return total_flow


# Create and populate the graph
G = nx.DiGraph()
edges = [
    ("A", "B", 10),
    ("B", "C", 5),
    ("A", "C", 15),
    ("C", "D", 10),
    ("B", "D", 10),
    ("D", "E", 10),
]
for u, v, capacity in edges:
    G.add_edge(u, v, capacity=capacity)

source = "A"
sink = "E"

# Calculate the maximum flow
max_flow = simple_flow_algorithm(G, source, sink)
print("The maximum flow from source to sink is:", max_flow)

# Drawing the graph with flow labels
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=700)
labels = {
    edge: f"{residual_capacity.get(edge, 0)}/{G[edge[0]][edge[1]]['capacity']}"
    for edge in G.edges()
}
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title("Flow Network")
plt.show()


# TODO: issue with residual capacity