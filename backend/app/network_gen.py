import random
from random import Random
import os

import networkx as nx
from backend.app.models import Node, InfectionStatus

from backend.util.node_initialization import *
from backend.util.probability_calculations import get_infection_prob, get_death_prob
import asyncio


def get_network(n, k, p):
    graph = nx.generators.random_graphs.watts_strogatz_graph(n, k, p)
    set_nodes(graph)

    return graph



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


