import React, { useEffect, useRef } from "react";
import Graph from "graphology";
import Sigma from "sigma";

export default function GraphView() {
    const containerRef = useRef(null);
    const sigmaRef = useRef(null);
    const graphRef = useRef(new Graph());

    useEffect(() => {
        let isMounted = true;

        const fetchData = async () => {
            try {
                const res = await fetch("http://localhost:8000/graph");
                if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
                const data = await res.json();

                if (!isMounted) return;

                graphRef.current.clear();

                // Add nodes with backend-provided coordinates
                data.nodes.forEach(node => {
                    graphRef.current.addNode(node.id, {
                        color: getColor(node.status),
                        size: 5,
                        x: node.x,  // Directly use backend x
                        y: node.y   // Directly use backend y
                    });
                });

                // Add edges
                data.edges.forEach(edge => {
                    graphRef.current.addEdge(edge.source, edge.target);
                });

                // Initialize/Update Sigma
                if (!sigmaRef.current) {
                    sigmaRef.current = new Sigma(
                        graphRef.current,
                        containerRef.current,
                        {
                            renderEdgeLabels: false,
                            enableEdgeClickEvents: false,
                            enableEdgeWheelEvents: false,
                            // Optional: Disable auto-rescale to use fixed coordinates
                            autoRescale: false
                        }
                    );
                } else {
                    sigmaRef.current.refresh();
                }

            } catch (err) {
                console.error("Failed to load graph:", err);
            }
        };

        fetchData();

        // Color update interval
        const interval = setInterval(async () => {
            try {
                const res = await fetch("http://localhost:8000/tick-updates");
                if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
                const data = await res.json();
                if (!isMounted) return;

                data.nodes.forEach(node => {
                    if (graphRef.current.hasNode(node.id)) {
                        graphRef.current.setNodeAttribute(
                            node.id,
                            "color",
                            getColor(node.status)
                        );
                    }
                });

                sigmaRef.current?.refresh();
            } catch (err) {
                console.error("Update failed:", err);
            }
        }, 500);

        return () => {
            isMounted = false;
            clearInterval(interval);
            sigmaRef.current?.kill();
        };
    }, []);

    return (
        <div ref={containerRef} style={{
            height: "100vh",
            width: "100%",
            backgroundColor: "#f0f0f0"
        }} />
    );
}

function getColor(status) {
    switch (status) {
        case "I": return "#ff0000";
        case "R": return "#00ff00";
        case "S": return "#ffd700";
        case "D": return "#000000";
        default: return "#cccccc";
    }
}