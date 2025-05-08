from random import randint

from backend.util.probability_calculations import get_death_prob, get_infection_prob
from backend.app.models import InfectionStatus
from backend.app.network_gen import get_network, set_nodes
from backend.util.node_initialization import generate_recovery_time

import asyncio
import random

avg = 0
count = 0

"""
    - CURRENTLY_INFECTED is the set of nodes which have infection status: INFECTED
    - RECOVERED is the set of nodes which have infection status: RECOVERED
    - TO_REMOVE is a set of nodes which have recovered or died.
    
    What is the point of these three sets?
        - On each tick, all nodes in CURRENTLY_INFECTED are traversed. For each infected node:
            i) Retrieve neighbors of that node.
            ii) For each neighbor, check if susceptible
            iii) if susceptible, assign infection probability
            iv) Use infection prob to see if neighbor gets infected
            v) if infected, add neighbor node to new_infections set
            vi) After iterating through all currently infected nodes, add new_infections to CURRENTLY_INFECTEDd
        
        - RECOVERED is required in order to revert recovered nodes to SUSCEPTIBLE after a specific number of ticks.
        
        - TO_REMOVE is used to update CURRENTLY_INFECTED by removing nodes which have died or recovered.
"""

CURRENTLY_INFECTED = set()
RECOVERED = set()
TO_REMOVE = set()
DECEASED = set()

TICK_INTERVAL = 0.25
simulation_running = True
current_tick = 0

def run_tick(graph):
    global current_tick
    new_infections = set()

    for node_id in list(RECOVERED):
        node_data = graph.nodes[node_id]['data']

        ticks_since_recovery = current_tick - node_data.recovery_tick
        if ticks_since_recovery >= 14:
            node_data.infection_status = InfectionStatus.SUSCEPTIBLE
            RECOVERED.remove(node_id)
            # print('i recovered yayyy')




    for node_id in list(CURRENTLY_INFECTED):

        node_data = graph.nodes[node_id]['data']

        infected_tick = node_data.infected_tick
        recovery_time = node_data.recovery_time
        death_probability = get_death_prob(node_data, current_tick)
        # print(death_probability)
        node_data.death_probability = death_probability

        rand = random.random()
        # avg += rand
        # count += 1
        # print(avg/count)
        if rand <= death_probability:
            kill(graph, node_id)
            continue


        if current_tick - infected_tick >= recovery_time:
            recover(graph, node_id)
            continue

        for neighbor_id in graph.neighbors(node_id):
            neighbor_data = graph.nodes[neighbor_id]['data']
            if neighbor_data.infection_status == InfectionStatus.SUSCEPTIBLE:


                edge = graph[node_id][neighbor_id]
                if 'infection_prob' not in edge:
                    edge['infection_prob'] = get_infection_prob(node_data, neighbor_data)


                if random.random() <= edge['infection_prob']:
                    infect(graph, neighbor_id)
                    new_infections.add(neighbor_id)

    CURRENTLY_INFECTED.update(new_infections)
    CURRENTLY_INFECTED.difference_update(TO_REMOVE)
    TO_REMOVE.clear()

    return new_infections



def infect(graph, node_id):
    global current_tick, count, avg
    node_data = graph.nodes[node_id]['data']
    node_data.infected_tick = current_tick
    node_data.death_probability = get_death_prob(node_data, current_tick)
    # print(node_data.death_probability)
    node_data.infection_status = InfectionStatus.INFECTED
    node_data.recovery_time = generate_recovery_time(node_data)
    CURRENTLY_INFECTED.add(node_id)


    for neighbor_id in graph.neighbors(node_id):

        neighbor_data = graph.nodes[neighbor_id]['data']
        graph[node_id][neighbor_id]['infection_prob'] = get_infection_prob(node_data, neighbor_data)
        # print(graph[node_id][neighbor_id]['infection_prob'])


def recover(graph, node_id):
    global current_tick

    node_data = graph.nodes[node_id]['data']
    node_data.infection_status = InfectionStatus.RECOVERED
    node_data.recovery_tick = current_tick
    RECOVERED.add(node_id)
    TO_REMOVE.add(node_id)

def kill(graph, node_id):
    graph.nodes[node_id]['data'].infection_status = InfectionStatus.DECEASED
    TO_REMOVE.add(node_id)
    DECEASED.add(node_id)
    pass

def randomly_infect(graph, num_infections):
    for _ in range(num_infections):
        infect(graph, randint(0, 5000))





async def simulate():
    global current_tick
    graph = get_network(5000, 4, 0.1)
    set_nodes(graph)

    randomly_infect(graph, 50)

    while simulation_running and CURRENTLY_INFECTED:
        visualize_graph_live(graph, current_tick)
        run_tick(graph)
        print("INFECTED: " + str(len(CURRENTLY_INFECTED)))
        print("RECOVERED: " + str(len(RECOVERED)))
        print("DECEASED: " + str(len(DECEASED)))
        print("TICKS:" + str(current_tick))
        current_tick += 1
        await asyncio.sleep(TICK_INTERVAL)



import matplotlib.pyplot as plt
import networkx as nx

# Calculate layout only once
POS = None

def visualize_graph_live(graph, tick):
    global POS
    if POS is None:
        POS = nx.spring_layout(graph, seed=42)  # Cache layout once

    color_map = []
    for node_id in graph.nodes:
        status = graph.nodes[node_id]['data'].infection_status

        if status == InfectionStatus.INFECTED:
            color_map.append('red')
        elif status == InfectionStatus.RECOVERED:
            color_map.append('green')
        elif status == InfectionStatus.SUSCEPTIBLE:
            color_map.append('yellow')
        elif status == InfectionStatus.DECEASED:
            color_map.append('black')
        else:
            color_map.append('gray')

    plt.clf()
    nx.draw(
        graph,
        POS,
        node_color=color_map,
        node_size=120,
        edge_color='lightgray',
        with_labels=False  # No labels for better performance
    )

    plt.title(f"Infection Spread at Tick {tick}")
    plt.pause(0.001)
