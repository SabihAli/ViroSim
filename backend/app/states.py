from backend.app.network_gen import get_network
from fa2_modified import ForceAtlas2
import asyncio

graph = get_network(30000, 4, 0.1)
forceatlas2 = ForceAtlas2(
    outboundAttractionDistribution=False,  # Disable edge weight influence
    scalingRatio=3.0,                          # Analogous to "k" in spring_layout
    strongGravityMode=False,
    jitterTolerance=0.5,
    gravity=0.1,                           # Central pull strength
    verbose=False                               # Reproducibility
)

# Calculate positions
pos = forceatlas2.forceatlas2_networkx_layout(graph, pos=None, iterations=100)

graph_lock = asyncio.Lock()