import React from "react";
import { SimulationProvider } from "./components/SimulationContext";
import Sidebar from "./components/SidebarView";
import GraphView from "./components/GraphView";

export default function App() {
    return (
        <SimulationProvider>
            <div style={{ display: "flex" }}>
                <Sidebar />
                <GraphView />
            </div>
        </SimulationProvider>
    );
}
