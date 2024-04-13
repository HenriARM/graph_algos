import networkx as nx
import matplotlib.pyplot as plt


class GraphVisualization:
    def __init__(self):
        self.graph = nx.Graph()

    def add_edge(self, node, neighbor):
        self.graph.add_edge(node, neighbor)

    def read_from_file(self, file_path):
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                # Ignore comments and blank lines
                if not line or line.startswith("#"):
                    continue
                # Parse the nodes and add the edge
                node, neighbor = map(int, line.split(","))
                # node, neighbor = line.split(",")
                self.add_edge(node, neighbor)

    def bfs(self, start):
        visited = set()
        queue = []
        order = {}
        height = {}  # New dictionary to keep track of heights of nodes

        queue.append((start, 0))  # Queue now stores tuples of (node, height)
        visited.add(start)
        order[start] = 0
        height[start] = 0  # Height of root is 0

        count = 1
        while queue:
            current, h = queue.pop(0)
            for neighbor in sorted(self.graph[current]):
                if neighbor not in visited:
                    queue.append((neighbor, h + 1))  # Increment height for child nodes
                    visited.add(neighbor)
                    order[neighbor] = count
                    height[neighbor] = h + 1  # Store the height of the neighbor
                    count += 1

        return order, height  # Return both order and height

    def dfs(self, start):
        visited = set()
        stack = []
        order = {}
        height = {}

        stack.append((start, 0))
        order[start] = 0
        height[start] = 0

        count = 1
        while stack:
            current, h = stack.pop()  # Pop from the stack to get the current node
            if current not in visited:
                visited.add(current)
                for neighbor in sorted(self.graph[current], reverse=True):  # Use sorted to process nodes numerically
                    if neighbor not in visited:
                        stack.append((neighbor, h + 1))
                order[current] = count
                count += 1

        return order, height
    def visualize(self, start=None):
        plt.figure(figsize=(10, 10))

        if start:
            order, _ = self.bfs(start)
            node_color = [
                order[node] if node in order else 0 for node in self.graph.nodes()
            ]
            labels = {
                # node: f"{node} ({order[node]})" if node in order else node
                node: f"{node}" if node in order else node
                for node in self.graph.nodes()
            }
        else:
            node_color = "skyblue"
            labels = {node: node for node in self.graph.nodes()}

        nx.draw_networkx(
            self.graph,
            labels=labels,
            node_size=2000,
            node_color=node_color,
            cmap=plt.cm.Blues,
            font_size=20,
            font_weight="bold",
        )
        plt.title(f"BFS from node {start}")
        plt.savefig("graph.png")
        # print nodes and their order
        print(order)
        # plt.show()

    def visualize_bfs_tree(self, start=None):
        if start is None:
            raise ValueError(
                "A starting node must be provided to visualize the BFS tree."
            )

        order, height = self.bfs(start)  # Get the height info as well

        # Calculate positions for nodes based on their height
        pos = nx.spring_layout(self.graph, iterations=100)
        for node, (x, y) in pos.items():
            pos[node] = (x, -height[node])  # Adjust y coordinate based on height

        node_color = [
            height[node] for node in self.graph.nodes()
        ]  # Color nodes based on height

        plt.figure(figsize=(12, 12), facecolor="white")
        # Draw nodes with varying color based on height and straight lines for edges
        nx.draw_networkx_edges(
            self.graph, pos, edge_color="gray", alpha=0.5, arrows=False
        )
        nx.draw_networkx_nodes(
            self.graph, pos, node_size=1000, node_color=node_color, cmap=plt.cm.viridis
        )
        nx.draw_networkx_labels(self.graph, pos, font_size=10, font_weight="bold")

        # Labels to indicate the height of the nodes
        label_pos = {k: (v[0], v[1] - 0.1) for k, v in pos.items()}
        nx.draw_networkx_labels(self.graph, label_pos, labels=order, font_color="red")

        plt.title(f"BFS Tree from node {start} with node heights")
        plt.axis("off")  # Hide the axes
        plt.savefig("bfs_tree_height.png", format="PNG", transparent=False)
        # plt.show()
        print("Order of nodes:", order)
        print("Height of nodes:", height)


if __name__ == "__main__":
    graph = GraphVisualization()
    graph.read_from_file("graph.txt")
    graph.visualize(start=4)
    graph.visualize_bfs_tree(start=4)

    # TODO: add DFS
    # TODO: visualize path between 2 nodes on tree
    # TODO: why each visualization is different? nodes are on different locations
    # TODO: visualize the graph so edges won't cross each other
    # TODO: add traversal_mode parameter to visualize method
