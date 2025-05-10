from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import networkx as nx
from backend.app.states import graph, pos, graph_lock  # Ensure graph_lock is asyncio.Lock
# from backend.app.sim_engine import tick_updates, simulate
import backend.app.sim_engine as sim_engine
import asyncio


app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def start_simulation():
    # Use asyncio.create_task() to run the simulation without blocking FastAPI
    asyncio.create_task(sim_engine.simulate(graph))

@app.get("/graph")
async def get_graph_data():  # Changed to async endpoint
    async with graph_lock:  # Proper async lock usage
        nodes = [
            {
                "id": n,
                "status": graph.nodes[n]["data"].infection_status.value,
                "x": pos[n][0],
                "y": pos[n][1]
            }
            for n in graph.nodes
        ]
        edges = [{"source": u, "target": v} for u, v in graph.edges]
    return {"nodes": nodes, "edges": edges}

@app.get("/tick-updates")
async def get_tick_updates():  # Changed to async endpoint
    async with graph_lock:  # Proper async lock usage
        updates = []
        for status_type, affected_nodes in sim_engine.tick_updates.items():
            updates.extend([
                {
                    "id": n,
                    "status": get_status(status_type),
                }
                for n in affected_nodes
            ])
        return {"nodes": updates}

def get_status(status_key: str) -> str:
    status_mapping = {
        "infected": "I",
        "recovered": "R",
        "deceased": "D",
        "susceptible": "S"
    }
    return status_mapping.get(status_key, "S")