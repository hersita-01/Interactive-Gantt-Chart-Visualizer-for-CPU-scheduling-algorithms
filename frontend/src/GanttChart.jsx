import React, { useEffect, useRef } from "react";
import * as d3 from "d3";

const GanttChart = ({ ganttData }) => {
  const svgRef = useRef();
  const containerRef = useRef();

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    // measure container to set SVG drawing area
    const rect = container.getBoundingClientRect();
    const width = Math.max(300, rect.width - 20);
    const height = Math.max(120, Math.min(240, rect.height - 60));
    const margin = { left: 40, right: 20, top: 10, bottom: 30 };

    const svg = d3.select(svgRef.current);
    svg.attr("viewBox", `0 0 ${width} ${height}`);
    svg.selectAll("*").remove();

    // ensure segments are rendered in chronological order
    const data = (ganttData || []).slice().sort((a, b) => a.start - b.start);
    const maxTime = d3.max(data, d => d.end) || 0;

    const xScale = d3.scaleLinear().domain([0, Math.max(1, maxTime)]).range([margin.left, width - margin.right]);

    // axis
    svg
      .append("g")
      .attr("transform", `translate(0, ${height - margin.bottom})`)
      .call(d3.axisBottom(xScale).ticks(Math.min(maxTime || 1, 10)).tickFormat(d3.format("d")))
      .selectAll("text")
      .style("font-size", "13px")
      .style("font-weight", 600)
      .style("fill", "#9aa4b2");

    // bars
    const barY = margin.top + 10;
    const barHeight = Math.max(28, height - margin.top - margin.bottom - 30);

    svg
      .selectAll("rect")
      .data(data)
      .enter()
      .append("rect")
      .attr("x", d => xScale(d.start))
      .attr("y", barY)
      .attr("width", d => Math.max(1, xScale(d.end) - xScale(d.start)))
      .attr("height", barHeight)
      .attr("fill", d => d.color || "#666")
      .attr("stroke", "rgba(0,0,0,0.6)");

    // labels
    svg
      .selectAll("text.labels")
      .data(data)
      .enter()
      .append("text")
      .attr("x", d => xScale((d.start + d.end) / 2))
      .attr("y", barY + barHeight / 2 + 5)
      .attr("text-anchor", "middle")
      .text(d => d.pid)
      .attr("fill", "white")
      .style("font-weight", "600")
      .style("pointer-events", "none")
      .style("font-size", Math.max(10, Math.min(14, barHeight / 3)) + "px");

  }, [ganttData]);

  return (
    <div ref={containerRef} className="gantt-wrap card" style={{minHeight: 160}}>
      <svg ref={svgRef} className="gantt-svg" preserveAspectRatio="xMidYMid meet" />
    </div>
  );
};

export default GanttChart;
