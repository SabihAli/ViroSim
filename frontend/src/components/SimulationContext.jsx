import React, { createContext, useContext, useEffect, useState } from "react";

const SimulationContext = createContext();

export const useSimulation = () => useContext(SimulationContext);

export const SimulationProvider = ({ children }) => {
    const [tick, setTick] = useState(0);
    const [counts, setCounts] = useState([]);
    const [latest, setLatest] = useState(null);
    const [isRunning, setIsRunning] = useState(true);

    useEffect(() => {
        const interval = setInterval(async () => {
            if (!isRunning) return;

            try {
                const res = await fetch("http://localhost:8000/count-updates");
                const data = await res.json();
                setTick(t => t + 1);
                setCounts(prev => [...prev, { tick, ...data }]);
                setLatest(data);
            } catch (err) {
                console.error("Sidebar fetch error:", err);
            }
        }, 500);

        return () => clearInterval(interval);
    }, [isRunning, tick]);

    return (
        <SimulationContext.Provider value={{
            tick, counts, latest, isRunning, setIsRunning, setTick, setCounts
        }}>
            {children}
        </SimulationContext.Provider>
    );
};
