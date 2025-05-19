from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import networkx as nx
import backend.app.states as states
from backend.app.states import graph, positions, graph_lock  # Ensure graph_lock is asyncio.Lock
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
    asyncio.create_task(sim_engine.simulate(states.graph))

@app.get("/graph")
async def get_graph_data():  # Changed to async endpoint
    async with states.graph_lock:  # Proper async lock usage
        nodes = [
            {
                "id": n,
                "status": states.graph.nodes[n]["data"].infection_status.value,
                "x": states.positions[n][0],
                "y": states.positions[n][1]
            }
            for n in states.graph.nodes
        ]
        # edges = [{"source": u, "target": v} for u, v in states.graph.edges]
    # return {"nodes": nodes, "edges": edges}
    return {"nodes": nodes}

@app.get("/tick-updates")
async def get_tick_updates():  # Changed to async endpoint
    async with states.graph_lock:  # Proper async lock usage
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

@app.get("/count-updates")
async def get_count_updates():
    async with states.graph_lock:
        i_count = len(sim_engine.CURRENTLY_INFECTED)
        r_count = len(sim_engine.RECOVERED)
        d_count = len(sim_engine.DECEASED)
        s_count = states.graph_size - i_count - r_count - d_count

    return {
        "infected": i_count,
        "recovered": r_count,
        "deceased": d_count,
        "susceptible": s_count
    }

def get_status(status_key: str) -> str:
    status_mapping = {
        "infected": "I",
        "recovered": "R",
        "deceased": "D",
        "susceptible": "S"
    }
    return status_mapping.get(status_key, "S")