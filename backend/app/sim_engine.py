from random import randint

from backend.util.probability_calculations import get_death_prob, get_infection_prob
from backend.app.models import InfectionStatus
from backend.util.node_initialization import generate_recovery_time
import backend.app.states as states

import asyncio
import random

avg = 0
count = 0

CURRENTLY_INFECTED = set()
RECOVERED = set()
TO_REMOVE = set()
DECEASED = set()

TICK_INTERVAL = 0.5
simulation_running = True
current_tick = 0
tick_updates = {}

def run_tick(graph):
    global current_tick
    new_infections = set()
    new_recoveries = set()
    new_deaths = set()
    re_susceptibles = set()

    for node_id in list(RECOVERED):
        node_data = graph.nodes[node_id]['data']
        ticks_since_recovery = current_tick - node_data.recovery_tick

        # Temporary immunity runs out, node becomes susceptible again
        if ticks_since_recovery >= 14:
            node_data.infection_status = InfectionStatus.SUSCEPTIBLE
            re_susceptibles.add(node_id)
            RECOVERED.remove(node_id)


    for node_id in list(CURRENTLY_INFECTED):
        node_data = graph.nodes[node_id]['data']
        infected_tick = node_data.infected_tick
        recovery_time = node_data.recovery_time
        death_probability = get_death_prob(node_data, current_tick)
        node_data.death_probability = death_probability

        # Death logic
        if random.random() <= death_probability:
            kill(graph, node_id)
            new_deaths.add(node_id)
            continue

        if current_tick - infected_tick >= recovery_time:
            recover(graph, node_id)
            new_recoveries.add(node_id)
            continue

        for neighbor_id in graph.neighbors(node_id):
            neighbor_data = graph.nodes[neighbor_id]['data']
            if neighbor_data.infection_status.value == "S":
                edge = graph[node_id][neighbor_id]
                if 'infection_prob' not in edge:
                    edge['infection_prob'] = get_infection_prob(node_data, neighbor_data)
                if random.random() <= edge['infection_prob']:
                    infect(graph, neighbor_id)
                    new_infections.add(neighbor_id)

    CURRENTLY_INFECTED.update(new_infections)
    CURRENTLY_INFECTED.difference_update(TO_REMOVE)
    TO_REMOVE.clear()

    return {
        "infected": list(new_infections),
        "recovered": list(new_recoveries),
        "deceased": list(new_deaths),
        "susceptible": list(re_susceptibles)
    }

def infect(graph, node_id):
    global current_tick
    node_data = graph.nodes[node_id]['data']
    node_data.infected_tick = current_tick
    node_data.death_probability = get_death_prob(node_data, current_tick)
    node_data.infection_status = InfectionStatus.INFECTED
    node_data.recovery_time = generate_recovery_time(node_data)
    CURRENTLY_INFECTED.add(node_id)

    for neighbor_id in graph.neighbors(node_id):
        neighbor_data = graph.nodes[neighbor_id]['data']
        graph[node_id][neighbor_id]['infection_prob'] = get_infection_prob(node_data, neighbor_data)

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

def randomly_infect(graph, num_infections):

    for _ in range(num_infections):
        infect(graph, randint(0, states.graph_size - 1))

async def simulate(graph):
    global current_tick, simulation_running, tick_updates

    async with states.graph_lock:
        randomly_infect(graph, 50)

    while simulation_running and CURRENTLY_INFECTED:
        async with states.graph_lock:
            tick_updates = run_tick(graph)


        print(f"INFECTED: {len(CURRENTLY_INFECTED)}")
        print(f"RECOVERED: {len(RECOVERED)}")
        print(f"DECEASED: {len(DECEASED)}")
        print(f"TICKS: {current_tick}")
        current_tick += 1
        await asyncio.sleep(TICK_INTERVAL)



def visualize_graph_live(graph, tick):
    global POS
    if POS is None:
        POS = nx.spring_layout(graph, seed=42)


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
