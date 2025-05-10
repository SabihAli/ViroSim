import React from "react";
import ReactDOM from "react-dom/client";
import GraphView from "./components/GraphView";
import App from "./App";


const root = ReactDOM.createRoot(document.getElementById("root"));  // Create root using createRoot

root.render(
    <React.StrictMode>
        {/*<GraphView />*/}
        <App />
    </React.StrictMode>
);
