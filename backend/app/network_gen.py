import random
from random import Random
import os

import networkx as nx
import matplotlib.pyplot as plt
from backend.app.models import Node, InfectionStatus
from backend.util.node_initialization import *
from backend.util.probability_calculations import get_infection_prob, get_death_prob
import asyncio


def get_network(n, k, p):
    return nx.generators.random_graphs.watts_strogatz_graph(n, k, p)


def set_nodes(graph : nx.Graph):

    for node_id in graph.nodes():
        infection_status = InfectionStatus.SUSCEPTIBLE
        age = generate_age()
        health_factor = generate_health_factor(1.25)
        mask_usage = generate_biased_bool(0.3)
        vax_status = generate_biased_bool(0.4)
        superspreader = generate_biased_bool(0.2)

        custom_node = Node(infection_status, age, health_factor, mask_usage, vax_status, superspreader)

        graph.nodes[node_id]['data'] = custom_node

#
# def set_edge_attributes(graph : nx.Graph):
#
#     for node_one_id, node_two_id in graph.edges():
#         node_one_data = graph.nodes[node_one_id]['data']
#         node_two_data = graph.nodes[node_two_id]['data']
#
#         graph[node_one_id][node_two_id]['infection_prob'] = get_infection_prob(node_one_data, node_two_data)



if __name__ == "__main__":
    social_network = get_network(5000, 4, 0.1)

    # pos = networkx.spring_layout(social_network.network, seed=42)  # seed for reproducibility
    # plt.figure(figsize=(8, 6))
    # networkx.draw(social_network.network, pos, node_size=50, node_color="skyblue", with_labels=False, edge_color="gray")
    # plt.title("Force-Directed Layout (Spring) of Watts-Strogatz Graph")
    # plt.axis('off')
    # plt.show()

    set_nodes(social_network)
    asyncio.run(simulate(social_network))

    # set_edge_attributes(social_network)


    # print("Infection status: " + social_network.nodes[3]['data'].infection_status.value)
    # print("Age: " + str(social_network.nodes[3]['data'].age))
    # print("health factor: " + str(social_network.nodes[3]['data'].health_factor))
    # print("Mask usage: " + str(social_network.nodes[3]['data'].mask_usage))
    # print("Vax status: " + str(social_network.nodes[3]['data'].vax_status))
    # print("Superspreader: " + str(social_network.nodes[3]['data'].superspreader))
    # print("temp immune: " + str(social_network.nodes[3]['data'].temp_immune))
    # max = -1
    # min = 2
    # sum = 0
    # for u, v, attr in social_network.edges(data=True):
    #     sum += attr['infection_prob']
    #
    #     if attr['infection_prob'] >= max:
    #         max = attr['infection_prob']
    #     if attr['infection_prob'] <= min:
    #         min = attr['infection_prob']
    #     print(f"Edge ({u}, {v}) has attributes: {attr}")
    #
    # print(max)
    # print(min)
    # print(sum/5000)


