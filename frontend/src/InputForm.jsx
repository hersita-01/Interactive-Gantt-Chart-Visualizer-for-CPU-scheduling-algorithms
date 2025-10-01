import React, { useState } from "react";

const InputForm = ({
  processes,
  setProcesses,
  selectedAlgorithm,
  setSelectedAlgorithm,
  timeQuantum,
  setTimeQuantum,
  runSimulation,
}) => {
  const [pid, setPid] = useState("");
  const [arrival, setArrival] = useState("");
  const [burst, setBurst] = useState("");
  const [priority, setPriority] = useState("");

  const addProcess = () => {
    if (!pid || !arrival || !burst) return alert("PID, Arrival, and Burst are required.");
    const newProc = { pid: String(pid).trim(), arrival_time: Number(arrival), burst_time: Number(burst), priority: Number(priority) || 0 };
    setProcesses(prev => [...prev, newProc]);
    setPid("");
    setArrival("");
    setBurst("");
    setPriority("");
  };

  const removeProcess = (index) => {
    setProcesses(prev => prev.filter((_, i) => i !== index));
  };

  return (
    <div className="input-form card">
      <h2>Process Input</h2>
      <div className="input-row">
        <input placeholder="PID" value={pid} onChange={e => setPid(e.target.value)} />
      </div>
      <div className="input-row">
        <input placeholder="Arrival Time" type="number" value={arrival} onChange={e => setArrival(e.target.value)} />
      </div>
      <div className="input-row">
        <input placeholder="Burst Time" type="number" value={burst} onChange={e => setBurst(e.target.value)} />
      </div>
      <div className="input-row">
        <input placeholder="Priority (optional)" type="number" value={priority} onChange={e => setPriority(e.target.value)} />
      </div>

      <div className="controls">
        <button className="btn-primary" onClick={addProcess}>Add Process</button>
        <button className="btn-ghost" onClick={() => setProcesses([])}>Clear</button>
      </div>

      {processes && processes.length > 0 && (
        <div className="card process-list">
          <h3>Added Processes</h3>
          <ul>
            {processes.map((p, idx) => (
              <li key={idx} className="process-row">
                <div className="process-desc">{p.pid} — arrival: {p.arrival_time ?? p.arrival} burst: {p.burst_time ?? p.burst}</div>
                <div><button className="small" onClick={() => removeProcess(idx)}>Remove</button></div>
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="algorithm-heading">Algorithm</div>
      <div className="algorithm-panel card">
        <div className="algorithm-options">
          <label><input type="radio" value="FCFS" checked={selectedAlgorithm === "FCFS"} onChange={e => setSelectedAlgorithm(e.target.value)} /> FCFS</label>
          <label><input type="radio" value="SJF" checked={selectedAlgorithm === "SJF"} onChange={e => setSelectedAlgorithm(e.target.value)} /> SJF</label>
          <label><input type="radio" value="SRTF" checked={selectedAlgorithm === "SRTF"} onChange={e => setSelectedAlgorithm(e.target.value)} /> SRTF</label>
          <label><input type="radio" value="RR" checked={selectedAlgorithm === "RR"} onChange={e => setSelectedAlgorithm(e.target.value)} /> Round Robin</label>
        </div>
      </div>

      {selectedAlgorithm === "RR" && (
        <div className="quantum-row">
          <input placeholder="Time Quantum" type="number" value={timeQuantum} onChange={e => setTimeQuantum(e.target.value)} />
        </div>
      )}

      <div style={{marginTop:'1rem'}}>
        <button className="btn-primary" onClick={runSimulation}>Run Simulation</button>
      </div>
    </div>
  );
};

export default InputForm;
