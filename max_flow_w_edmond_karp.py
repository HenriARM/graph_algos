import networkx as nx
import matplotlib.pyplot as plt

def edmonds_karp_max_flow(graph, source, sink):
    # Create a directed graph
    G = nx.DiGraph()
    
    # Add edges along with their capacities to the graph
    for u, v, capacity in graph:
        G.add_edge(u, v, capacity=capacity)
    
    # Compute the maximum flow between the source and the sink using the Edmonds-Karp algorithm
    flow_value, flow_dict = nx.maximum_flow(G, source, sink, flow_func=nx.algorithms.flow.edmonds_karp)
    
    return G, flow_value, flow_dict

def plot_graph(G, flow_dict, source, sink):
    # Position nodes using the spring layout
    pos = nx.spring_layout(G)
    
    # Draw the network graph nodes
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=700)
    
    # Draw the labels for the nodes
    nx.draw_networkx_labels(G, pos)
    
    # Edges are drawn with their flow and capacity
    edge_labels = {(u, v): f"{flow_dict[u][v]}/{G[u][v]['capacity']}" for u, v in G.edges()}
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrowstyle='-|>', arrowsize=20)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title("Network Flow Visualization")
    plt.show()

# Example usage
graph_edges = [
    ('A', 'B', 10),
    ('A', 'C', 5),
    ('B', 'C', 15),
    ('B', 'D', 9),
    ('C', 'D', 4),
    ('C', 'E', 8),
    ('D', 'E', 15),
    ('E', 'F', 10),
    ('D', 'F', 10)
]
source = 'A'
sink = 'F'

# Get the maximum flow and the flow along each edge
G, max_flow, flow_edges = edmonds_karp_max_flow(graph_edges, source, sink)
print("Maximum Flow:", max_flow)
print("Flow along edges:", flow_edges)

# Plot the graph
plot_graph(G, flow_edges, source, sink)



# TODO: plot source sink from left to right (hierarchical or layered layout of pygraphviz dot layout)
