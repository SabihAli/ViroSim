import React from "react";
import ReactDOM from "react-dom/client";
import GraphView from "./GraphView";

const root = ReactDOM.createRoot(document.getElementById("root"));  // Create root using createRoot

root.render(
    <React.StrictMode>
        <GraphView />
    </React.StrictMode>
);
