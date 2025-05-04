from random import Random
import os

import networkx as nx
import matplotlib.pyplot as plt
from backend.app.models import Node, InfectionStatus
from backend.util.node_initialization import *



def get_network(n, k, p):
    return nx.generators.random_graphs.watts_strogatz_graph(n, k, p)


def set_nodes(graph : nx.Graph):

    for node in graph.nodes():
        infection_status = InfectionStatus.SUSCEPTIBLE
        age = generate_age()
        health_factor = generate_health_factor(2)
        mask_usage = generate_biased_bool(0.39)
        vax_status = generate_biased_bool(0.6)
        superspreader = generate_biased_bool(0.15)
        temp_immune = True if infection_status == 'R' else False

        custom_node = Node(infection_status, age, health_factor, mask_usage, vax_status, superspreader, temp_immune)

        graph.nodes[node]['data'] = custom_node


def set_edge_weight(graph : nx.Graph):

    for node_one, node_two in graph.edges():




if __name__ == "__main__":
    social_network = get_network(5000, 4, 0.1)

    # pos = networkx.spring_layout(social_network.network, seed=42)  # seed for reproducibility
    # plt.figure(figsize=(8, 6))
    # networkx.draw(social_network.network, pos, node_size=50, node_color="skyblue", with_labels=False, edge_color="gray")
    # plt.title("Force-Directed Layout (Spring) of Watts-Strogatz Graph")
    # plt.axis('off')
    # plt.show()

    set_nodes(social_network)

    print("Infection status: " + social_network.nodes[3]['data'].infection_status.value)
    print("Age: " + str(social_network.nodes[3]['data'].age))
    print("health factor: " + str(social_network.nodes[3]['data'].health_factor))
    print("Mask usage: " + str(social_network.nodes[3]['data'].mask_usage))
    print("Vax status: " + str(social_network.nodes[3]['data'].vax_status))
    print("Superspreader: " + str(social_network.nodes[3]['data'].superspreader))
    print("temp immune: " + str(social_network.nodes[3]['data'].temp_immune))


