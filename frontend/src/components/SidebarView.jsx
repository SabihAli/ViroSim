// Sidebar.jsx
import React from "react";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import PauseIcon from "@mui/icons-material/Pause";
import StopIcon from "@mui/icons-material/Stop";
import {
    LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid,
    PieChart, Pie, Cell, ResponsiveContainer
} from "recharts";
import { useSimulation } from "./SimulationContext";

const COLORS = {
    infected: "#ff4d4f",
    susceptible: "#7c4dff",
    recovered: "#4dff88",
    deceased: "#8e8e8e"
};

const BG_COLOR = "#1a1a1a";
const TEXT_COLOR = "#f0f0f0";
const GRID_COLOR = "#2d2d2d";

export default function Sidebar() {
    const { counts, latest, isRunning, setIsRunning, setCounts, setTick } = useSimulation();

    const handlePause = () => setIsRunning(false);
    const handlePlay = () => setIsRunning(true);
    const handleStop = () => {
        setIsRunning(false);
        setCounts([]);
        setTick(0);
    };

    return (
        <div style={{
            width: "320px",
            padding: "24px",
            display: "flex",
            flexDirection: "column",
            background: `linear-gradient(145deg, ${BG_COLOR}, #1f1f1f)`,
            color: TEXT_COLOR,
            gap: "24px",
            borderRight: "1px solid #2d2d2d",
            fontFamily: "'Inter', sans-serif",
            boxShadow: "4px 0 12px rgba(0,0,0,0.3)"
        }}>
            <h2 style={{
                margin: "0 0 16px 0",
                color: TEXT_COLOR,
                fontFamily: "'Inter', sans-serif",
                fontWeight: 600,
                fontSize: "1.4rem",
                textAlign: "center",
                letterSpacing: "-0.5px",
                position: "relative",
                paddingBottom: "12px",
                borderBottom: "1px solid #333"
            }}>
                Simulation Dashboard
                <span style={{
                    position: "absolute",
                    bottom: "-2px",
                    left: "50%",
                    transform: "translateX(-50%)",
                    width: "40px",
                    height: "2px",
                    background: COLORS.infected,
                    borderRadius: "2px"
                }} />
            </h2>

            {/* Line Chart */}
            <div style={{
                height: "180px",
                borderRadius: "12px",
                overflow: "hidden",
                background: "#202020",
                padding: "12px",
                boxShadow: "inset 0 0 8px rgba(0,0,0,0.2)"
            }}>
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={counts}>
                        <CartesianGrid stroke={GRID_COLOR} strokeDasharray="3 3" />
                        <XAxis
                            dataKey="tick"
                            stroke={TEXT_COLOR}
                            tick={{ fontSize: 10 }}
                            tickLine={{ stroke: GRID_COLOR }}
                        />
                        <YAxis
                            stroke={TEXT_COLOR}
                            tick={{ fontSize: 10 }}
                            tickLine={{ stroke: GRID_COLOR }}
                        />
                        <Tooltip
                            contentStyle={{
                                background: "#2b2b2b",
                                border: "1px solid #383838",
                                borderRadius: "6px",
                                boxShadow: "0 4px 12px rgba(0,0,0,0.3)"
                            }}
                            itemStyle={{ padding: 0 }}
                        />
                        <Line
                            type="monotone"
                            dataKey="infected"
                            stroke={COLORS.infected}
                            strokeWidth={1.5}
                            dot={false}
                        />
                        <Line
                            type="monotone"
                            dataKey="susceptible"
                            stroke={COLORS.susceptible}
                            strokeWidth={1.5}
                            dot={false}
                        />
                        <Line
                            type="monotone"
                            dataKey="recovered"
                            stroke={COLORS.recovered}
                            strokeWidth={1.5}
                            dot={false}
                        />
                        <Line
                            type="monotone"
                            dataKey="deceased"
                            stroke={COLORS.deceased}
                            strokeWidth={1.5}
                            dot={false}
                        />
                    </LineChart>
                </ResponsiveContainer>
            </div>

            {/* Pie Chart & Stats */}
            <div style={{
                display: "grid",
                gridTemplateColumns: "1fr 1fr",
                gap: "18px",
                background: "#202020",
                borderRadius: "12px",
                padding: "16px",
                boxShadow: "inset 0 0 8px rgba(0,0,0,0.2)"
            }}>
                {latest && (
                    <div style={{ position: "relative" }}>
                        <PieChart width={140} height={140}>
                            <Pie
                                dataKey="value"
                                cx="50%"
                                cy="50%"
                                innerRadius={35}
                                outerRadius={55}
                                data={[
                                    { name: "Infected", value: latest.infected },
                                    { name: "Susceptible", value: latest.susceptible },
                                    { name: "Recovered", value: latest.recovered },
                                    { name: "Deceased", value: latest.deceased }
                                ]}
                                paddingAngle={2}
                            >
                                {Object.keys(COLORS).map((key, index) => (
                                    <Cell
                                        key={index}
                                        fill={COLORS[key]}
                                        stroke="#1a1a1a"
                                        strokeWidth={2}
                                    />
                                ))}
                            </Pie>
                            <text
                                x="50%"
                                y="50%"
                                textAnchor="middle"
                                fill={TEXT_COLOR}
                                dy={4}
                                style={{
                                    fontSize: "0.8rem",
                                    fontWeight: 500,
                                    letterSpacing: "-0.5px"
                                }}
                            >
                                {latest.total}
                                <tspan x="50%" dy={16} style={{ fontSize: "0.6rem" }}>Total</tspan>
                            </text>
                        </PieChart>
                    </div>
                )}

                <div style={{
                    display: "flex",
                    flexDirection: "column",
                    gap: "8px",
                    justifyContent: "center"
                }}>
                    {latest && Object.entries(latest).map(([key, value]) => (
                        <div key={key} style={{
                            display: "flex",
                            alignItems: "center",
                            gap: "8px"
                        }}>
                            <div style={{
                                width: "10px",
                                height: "10px",
                                borderRadius: "2px",
                                background: COLORS[key],
                                flexShrink: 0
                            }} />
                            <div style={{
                                fontSize: "0.85rem",
                                color: "#d0d0d0",
                                display: "flex",
                                justifyContent: "space-between",
                                width: "115px"
                            }}>
                                <span>{key.charAt(0).toUpperCase() + key.slice(1)}</span>
                                <span style={{ fontWeight: 500 }}>{value}</span>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Controls */}
            <div style={{
                display: 'flex',
                justifyContent: 'center',
                gap: '16px',
                marginTop: '12px'
            }}>
                <ControlButton onClick={handlePlay} isActive={!isRunning}>
                    <PlayArrowIcon style={{ fontSize: "1.8rem" }} />
                </ControlButton>
                <ControlButton onClick={handlePause} isActive={isRunning}>
                    <PauseIcon style={{ fontSize: "1.8rem" }} />
                </ControlButton>
                <ControlButton onClick={handleStop}>
                    <StopIcon style={{ fontSize: "1.8rem" }} />
                </ControlButton>
            </div>
        </div>
    );
}

function ControlButton({ onClick, children, isActive }) {
    return (
        <button
            onClick={onClick}
            style={{
                width: "48px",
                height: "48px",
                borderRadius: "10px",
                background: isActive ? "#2b2b2b" : "#363636",
                border: "none",
                color: isActive ? COLORS.infected : "#d0d0d0",
                cursor: "pointer",
                transition: "all 0.2s cubic-bezier(0.4, 0, 0.2, 1)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                boxShadow: "0 4px 6px rgba(0,0,0,0.15)",
                ":hover": {
                    background: "#404040",
                    color: "#fff",
                    transform: "translateY(-1px)",
                    boxShadow: "0 6px 8px rgba(0,0,0,0.25)"
                },
                ":active": {
                    transform: "translateY(0)",
                    boxShadow: "0 2px 4px rgba(0,0,0,0.2)"
                }
            }}
        >
            {children}
        </button>
    );
}