import networkx as nx
import matplotlib.pyplot as plt

# Define the graph based on the adjacency list
graph_data = {
    1: [2, 3, 7, 10],
    2: [1, 3, 4],
    3: [1, 2, 6, 7, 10],
    4: [2, 5, 6, 7, 8],
    5: [4, 9],
    6: [3, 4, 7, 10],
    7: [1, 3, 4, 6, 10],
    8: [4, 9],
    9: [5, 8, 10],
    10: [1, 3, 6, 7, 9],
}


# Create a NetworkX graph
G = nx.Graph(graph_data)

# Different strategies for greedy coloring
strategies = ["largest_first", "smallest_last", "random_sequential", "independent_set"]


def plot_coloring(graph, coloring, title, strategy):
    colors = [coloring[node] for node in graph.nodes()]
    pos = nx.spring_layout(graph, seed=42)
    plt.figure(figsize=(10, 10))
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=colors,
        node_size=800,
        font_size=16,
        cmap=plt.cm.rainbow,
    )
    plt.title(title)
    plt.savefig(f"{strategy}.png")


colorings = {}

for strategy in strategies:
    coloring = nx.coloring.greedy_color(G, strategy=strategy)
    colorings[strategy] = coloring
    plot_coloring(
        G,
        coloring,
        f'Graph Coloring using {strategy.replace("_", " ").title()} Strategy',
        strategy
    )

colorings
