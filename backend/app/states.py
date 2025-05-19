import json
import os.path
import pickle

from backend.app.network_gen import get_network
from fa2_modified import ForceAtlas2
import asyncio

graph_size = 15000
positions_path = "backend/data/positions.json"
graph_path = "backend/data/graph.pkl"


current_tick = 0
CURRENTLY_INFECTED = set()
RECOVERED = set()
DECEASED = set()
TO_REMOVE = set()
TICK_INTERVAL = 0.25

graph_lock = asyncio.Lock()

def get_graph():
    if os.path.exists(graph_path):
        with open(graph_path, "rb") as f:
            return pickle.load(f)
    else:
        G = get_network(graph_size, 4, 0.1)

        with open(graph_path, "wb") as f:
            pickle.dump(G, f)

        return G


def get_positions():
    if os.path.exists(positions_path):
        print("hi")
        with open(positions_path, "r") as f:
            pos = json.load(f)

        return {int(k): v for k, v in pos.items()}
    else:
        forceatlas2 = ForceAtlas2(
            outboundAttractionDistribution=False,  # Disable edge weight influence
            scalingRatio=3.0,  # Analogous to "k" in spring_layout
            strongGravityMode=False,
            jitterTolerance=0.5,
            gravity=0.1,  # Central pull strength
            verbose=False  # Reproducibility
        )

        pos = forceatlas2.forceatlas2_networkx_layout(graph, pos=None, iterations=100)

        with open(positions_path, "w") as f:
           json.dump(pos, f)

        return pos


graph = get_graph()
positions = get_positions()