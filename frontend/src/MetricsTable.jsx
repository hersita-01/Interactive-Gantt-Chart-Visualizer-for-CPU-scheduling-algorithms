import React from "react";

const MetricsTable = ({ metrics, averages, ganttData = [] }) => {
  // compute CPU utilization: total busy time / timeline end
  const maxEnd = ganttData.reduce((m, s) => Math.max(m, s.end || 0), 0);
  const busy = ganttData.reduce((sum, s) => sum + Math.max(0, (s.end || 0) - (s.start || 0)), 0);
  const cpuUtil = maxEnd > 0 ? Math.min(100, Math.round((busy / maxEnd) * 10000) / 100) : 0;

  return (
    <div className="metrics-table card"> {/* Removed light-card */}
      <h3 style={{marginTop:0, marginBottom:8, fontSize:'1rem', color: 'var(--text)'}}>Final Performance Metrics</h3>

      <div className="metric-summaries">
        <div className="metric-box">
          <div className="metric-label">Average Waiting Time</div>
          <div className="metric-value">{typeof averages.awt !== 'undefined' ? averages.awt : 0}</div>
        </div>
        <div className="metric-box">
          <div className="metric-label">Average Turnaround Time</div>
          <div className="metric-value">{typeof averages.att !== 'undefined' ? averages.att : 0}</div>
        </div>
        <div className="metric-box">
          <div className="metric-label">CPU Utilization</div>
          <div className="metric-value">{cpuUtil}%</div>
        </div>
      </div>

      <div style={{marginTop:6, marginBottom:6, color:'var(--muted)'}}>Detailed Calculations</div>

      <table className="process-metrics-table" style={{width:'100%'}}>
        <thead>
          <tr>
            <th>Process</th>
            <th>Arrival</th>
            <th>Burst</th>
            <th>Completion</th>
            <th>Turnaround</th>
            <th>Waiting</th>
          </tr>
        </thead>
        <tbody>
          {metrics.map(m => (
            <tr key={m.pid}>
              <td>{m.pid}</td>
              <td>{m.arrival_time ?? m.arrival}</td>
              <td>{m.burst_time ?? m.burst}</td>
              <td>{m.completion_time ?? m.completion}</td>
              <td>{m.turnaround_time}</td>
              <td>{m.waiting_time}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default MetricsTable;