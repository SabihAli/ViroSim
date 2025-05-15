from backend.app.network_gen import get_network
from fa2_modified import ForceAtlas2
import asyncio

forceatlas2 = ForceAtlas2(
    outboundAttractionDistribution=False,  # Disable edge weight influence
    scalingRatio=3.0,                          # Analogous to "k" in spring_layout
    strongGravityMode=False,
    jitterTolerance=0.5,
    gravity=0.1,                           # Central pull strength
    verbose=False                               # Reproducibility
)

graph_size = 15000
graph = get_network(graph_size, 4, 0.1)
pos = forceatlas2.forceatlas2_networkx_layout(graph, pos=None, iterations=100)


current_tick = 0
CURRENTLY_INFECTED = set()
RECOVERED = set()
DECEASED = set()
TO_REMOVE = set()
TICK_INTERVAL = 0.25

graph_lock = asyncio.Lock()
