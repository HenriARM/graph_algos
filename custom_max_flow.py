import networkx as nx
import matplotlib.pyplot as plt
import os
import imageio.v2 as imageio

def custom_edmonds_karp(G, source, sink, folder):
    # Initialize residual graph with capacity as initial flow
    R = nx.DiGraph()
    for u, v, data in G.edges(data=True):
        R.add_edge(u, v, capacity=data['capacity'], flow=0)

    pos = nx.spring_layout(G)  # Fixed positions for all nodes
    os.makedirs(folder, exist_ok=True)  # Ensure folder exists

    def plot_graph(step):
        plt.figure(figsize=(8, 6))
        # nodes
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)
        # edges
        labels = { (u, v): f"{R[u][v]['flow']}/{R[u][v]['capacity']}" for u, v in R.edges()}
        nx.draw_networkx_edges(G, pos, edgelist=R.edges(), width=1)
        nx.draw_networkx_labels(G, pos, font_size=12, font_family="sans-serif")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.title(f"Flow After Step {step}")
        plt.axis("off")
        plt.savefig(os.path.join(folder, f"step_{step:03}.png"))
        plt.close()

    max_flow = 0
    step = 0
    while True:
        # Find path with BFS
        path = []
        queue = [source]
        paths = {source: []}
        if source == sink:
            break
        while queue:
            u = queue.pop(0)
            for v in G.neighbors(u):
                if v not in paths and R[u][v]['capacity'] - R[u][v]['flow'] > 0:
                    paths[v] = paths[u] + [(u, v)]
                    if v == sink:
                        path = paths[v]
                        break
                    queue.append(v)
            if path:
                break

        if not path:
            break  # no path found, we are done

        # Find the maximum flow on the path
        flow = min(R[u][v]['capacity'] - R[u][v]['flow'] for u, v in path)
        for u, v in path:
            R[u][v]['flow'] += flow
            if R.has_edge(v, u):
                R[v][u]['flow'] -= flow
            else:
                R.add_edge(v, u, capacity=0, flow=-flow)

        max_flow += flow
        step += 1
        print(f"Step {step}: Augmented Path: {[(u, v) for u, v in path]} with flow {flow}")
        plot_graph(step)

    return max_flow

# Create a directed graph
G = nx.DiGraph()
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
for u, v, capacity in graph_edges:
    G.add_edge(u, v, capacity=capacity)

source = 'A'
sink = 'F'
folder = 'flow_steps'

# Get the maximum flow
max_flow = custom_edmonds_karp(G, source, sink, folder)
print("Maximum Flow:", max_flow)

# Create a GIF
images = []
for file_name in sorted(os.listdir(folder)):
    if file_name.endswith('.png'):
        file_path = os.path.join(folder, file_name)
        images.append(imageio.imread(file_path))
imageio.mimsave(os.path.join(folder, 'flow_animation.gif'), images, duration=10)


# TODO: make plot change slower