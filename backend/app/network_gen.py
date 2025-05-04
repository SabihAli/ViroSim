import networkx
import matplotlib.pyplot as plt

class SocialNetwork:
    def __init__(self):
        self.network = networkx.generators.random_graphs.watts_strogatz_graph(5000, 3, 0.1)



if __name__ == "__main__":
    social_network = SocialNetwork()

    pos = networkx.spring_layout(social_network.network, seed=42)  # seed for reproducibility
    plt.figure(figsize=(8, 6))
    networkx.draw(social_network.network, pos, node_size=50, node_color="skyblue", with_labels=False, edge_color="gray")
    plt.title("Force-Directed Layout (Spring) of Watts-Strogatz Graph")
    plt.axis('off')
    plt.show()


