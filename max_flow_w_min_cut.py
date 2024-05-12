import networkx as nx
import matplotlib.pyplot as plt

def plot_graph_with_min_cut(G, source, sink, cut_set):
    pos = nx.spring_layout(G)  # positions for all nodes
    
    # Nodes
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=700)
    
    # Edges
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='gray')
    
    # Highlighting the cut edges
    cut_edges = [(u, v) for u in cut_set[0] for v in cut_set[1] if G.has_edge(u, v)]
    nx.draw_networkx_edges(G, pos, edgelist=cut_edges, edge_color='red', style='dashed')
    
    # Labels
    nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')
    labels = { (u, v): f"{d['capacity']}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    plt.title("Network Graph with Min-Cut Highlighted")
    plt.axis("off")
    plt.show()

def find_max_flow_min_cut(graph_edges, source, sink):
    G = nx.DiGraph()
    for u, v, capacity in graph_edges:
        G.add_edge(u, v, capacity=capacity)
    
    # Compute maximum flow and minimum cut
    cut_value, cut_set = nx.minimum_cut(G, source, sink)
    print("Maximum Flow / Min-Cut Value:", cut_value)
    print("Min-Cut Sets:", cut_set)

    return G, cut_set

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

# Get the graph and min-cut
G, cut_set = find_max_flow_min_cut(graph_edges, source, sink)

# Plot the graph with min-cut highlighted
plot_graph_with_min_cut(G, source, sink, cut_set)
