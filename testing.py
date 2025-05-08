from backend.app.network_gen import get_network, set_nodes
from backend.app.sim_engine import simulate
import asyncio


asyncio.run(simulate())