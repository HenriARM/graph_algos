import networkx as nx
import matplotlib.pyplot as plt

def find_max_flow_min_cost(graph_edges, source, sink):
    G = nx.DiGraph()
    for u, v, capacity, cost in graph_edges:
        G.add_edge(u, v, capacity=capacity, weight=cost)

    # Prepare for the minimum cost flow calculation
    # Set the demand for source as the sum of capacities leading from source
    # and the demand for sink as negative of this sum
    demand = sum(capacity for u, v, capacity, cost in graph_edges if u == source)
    G.nodes[source]['demand'] = -demand
    G.nodes[sink]['demand'] = demand

    # Calculate minimum cost flow
    flow_dict = nx.min_cost_flow(G)

    return G, flow_dict

def plot_graph(G, flow_dict):
    pos = nx.spring_layout(G)  # positions for all nodes
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=700)
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='gray')
    
    # Labels for nodes and edges
    nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')
    edge_labels = {(u, v): f"{flow_dict[u][v]}/{G[u][v]['capacity']}, ${G[u][v]['weight']}" for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title("Network Graph with Minimum Cost Flow")
    plt.axis("off")
    plt.show()

# Example usage
graph_edges = [
    ('A', 'B', 10, 2),
    ('A', 'C', 5, 1),
    ('B', 'C', 15, 1),
    ('B', 'D', 9, 3),
    ('C', 'D', 4, 1),
    ('C', 'E', 8, 2),
    ('D', 'E', 15, 2),
    ('E', 'F', 10, 1),
    ('D', 'F', 10, 4)
]
source = 'A'
sink = 'F'

# Get the graph and flow dictionary
G, flow_dict = find_max_flow_min_cost(graph_edges, source, sink)

# Plot the graph with minimum cost flow
plot_graph(G, flow_dict)
