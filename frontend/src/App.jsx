import React, { useState } from "react";
import InputForm from "./InputForm";
import GanttChart from "./GanttChart";
import MetricsTable from "./MetricsTable";
import "./App.css";
import { schedule } from "./api";

function App() {
  const [processes, setProcesses] = useState([]);
  const [selectedAlgorithm, setSelectedAlgorithm] = useState("FCFS");
  const [timeQuantum, setTimeQuantum] = useState(4);
  const [ganttData, setGanttData] = useState([]);
  const [metrics, setMetrics] = useState([]);
  const [averages, setAverages] = useState({ att: 0, awt: 0 });

  const runSimulation = async () => {
    if (processes.length === 0) return alert("Add at least one process.");

    // Normalize frontend process objects to the backend expected shape
    const normalized = processes.map((p) => ({
      pid: String(p.pid),
      arrival_time: Number(p.arrival || p.arrival_time || 0),
      burst_time: Number(p.burst || p.burst_time || 0),
      priority: Number(p.priority || 0),
      time_quantum: Number(p.timeQuantum || p.time_quantum || 0),
    }));

    try {
      const resp = await schedule(selectedAlgorithm, normalized, selectedAlgorithm === "RR" ? Number(timeQuantum) : null);
      // backend returns gantt_data, metrics, averages
      setGanttData(resp.gantt_data || []);
      setMetrics(resp.metrics || []);
      setAverages(resp.averages || { awt: 0, att: 0 });
    } catch (err) {
      console.error("Scheduling API error", err);
      alert("Scheduling API error: " + (err.message || err));
    }
  };

  return (
    <div className="app-root">
      <div className="container">
        <div className="header">
          <h1 className="title">OS Scheduling Simulator by Hersita Chandak</h1>
          <div className="subtitle">Visualize scheduling algorithms and process metrics</div>
        </div>
        <div className="layout">
        <div className="left">
          <InputForm
            processes={processes}
            setProcesses={setProcesses}
            selectedAlgorithm={selectedAlgorithm}
            setSelectedAlgorithm={setSelectedAlgorithm}
            timeQuantum={timeQuantum}
            setTimeQuantum={setTimeQuantum}
            runSimulation={runSimulation}
          />
        </div>
        <div className="right">
          <div className="visuals">
            <div className="gantt-panel card">
              <h2>Gantt Chart</h2>
              <GanttChart ganttData={ganttData} />
            </div>
            <div className="metrics-panel card">
              <h2>Process Metrics</h2>
              <MetricsTable metrics={metrics} averages={averages} />
            </div>
          </div>
        </div>
        </div>
      </div>
    </div>
  );
}

export default App;
