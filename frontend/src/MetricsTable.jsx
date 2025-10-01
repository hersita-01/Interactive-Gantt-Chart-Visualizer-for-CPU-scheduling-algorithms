import React from "react";

const MetricsTable = ({ metrics, averages }) => {
  return (
    <div className="metrics-table card">
      <h3>Process Metrics</h3>
      <table>
        <thead>
          <tr>
            <th>PID</th>
            <th>Turnaround Time</th>
            <th>Waiting Time</th>
          </tr>
        </thead>
        <tbody>
          {metrics.map(m => (
            <tr key={m.pid}>
              <td>{m.pid}</td>
              <td>{m.turnaround_time}</td>
              <td>{m.waiting_time}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="averages">
        <div><strong>Average Turnaround Time (ATT):</strong> {averages.att}</div>
        <div><strong>Average Waiting Time (AWT):</strong> {averages.awt}</div>
      </div>
    </div>
  );
};

export default MetricsTable;
