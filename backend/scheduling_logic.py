# scheduling_logic.py
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Any

# A small palette for Gantt chart colors
COLOR_PALETTE = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
]


@dataclass
class Process:
    """
    Process model holding inputs and simulation outputs.
    """
    pid: str
    arrival_time: int
    burst_time: int
    priority: int = 0
    time_quantum: int = 0

    # simulation state fields (initialized post-construction)
    remaining: int = field(init=False)
    completion_time: int = field(default=None)
    turnaround_time: int = field(default=None)
    waiting_time: int = field(default=None)
    started: bool = field(default=False)

    def __post_init__(self):
        # remaining execution time starts equal to burst_time
        self.remaining = int(self.burst_time)


def _assign_colors(pids: List[str]) -> Dict[str, str]:
    """
    Assign a deterministic color to each pid using a fixed palette.
    """
    colors = {}
    palette = COLOR_PALETTE
    for i, pid in enumerate(sorted(pids)):
        colors[pid] = palette[i % len(palette)]
    return colors


def _merge_segments(segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Merge consecutive segments with the same pid to produce cleaner Gantt segments.
    """
    if not segments:
        return []
    merged = [segments[0].copy()]
    for seg in segments[1:]:
        last = merged[-1]
        if seg["pid"] == last["pid"] and seg["start"] == last["end"]:
            last["end"] = seg["end"]
        else:
            merged.append(seg.copy())
    return merged


def _finalize_metrics(processes: List[Process]) -> Tuple[List[Dict[str, Any]], Dict[str, float]]:
    """
    Compute turnaround and waiting times and averages for all processes.
    """
    metrics = []
    total_wt = 0
    total_tt = 0
    n = len(processes)
    for p in sorted(processes, key=lambda x: x.pid):
        # completion_time must be already set by the scheduler
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time
        metrics.append({
            "pid": p.pid,
            "completion_time": p.completion_time,
            "turnaround_time": p.turnaround_time,
            "waiting_time": p.waiting_time
        })
        total_wt += p.waiting_time
        total_tt += p.turnaround_time
    averages = {
        "awt": round(total_wt / n, 2) if n else 0,
        "att": round(total_tt / n, 2) if n else 0
    }
    return metrics, averages


def fcfs(process_list: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, float]]:
    """
    First-Come, First-Served scheduling (non-preemptive).
    Simulates tick-by-tick by advancing the time equal to the burst length for each process.
    """
    processes = [Process(**p) for p in process_list]
    # sort by arrival then pid for deterministic ordering
    processes.sort(key=lambda x: (x.arrival_time, x.pid))
    colors = _assign_colors([p.pid for p in processes])

    time = 0
    gantt = []

    for p in processes:
        if time < p.arrival_time:
            # idle until the process arrives
            time = p.arrival_time
        start = time
        # simulate the process running for its full burst (tick-by-tick conceptually)
        for _ in range(p.burst_time):
            time += 1
        end = time
        p.completion_time = end
        gantt.append({"pid": p.pid, "start": start, "end": end, "color": colors[p.pid]})

    gantt = _merge_segments(gantt)
    metrics, averages = _finalize_metrics(processes)
    return gantt, metrics, averages


def sjf_non_preemptive(process_list: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, float]]:
    """
    Shortest Job First (non-preemptive).
    At each scheduling decision, pick the ready process with the smallest burst time.
    """
    processes = [Process(**p) for p in process_list]
    colors = _assign_colors([p.pid for p in processes])
    n = len(processes)
    completed = 0
    time = 0
    gantt = []
    ready = []

    while completed < n:
        # add arrived processes to ready list
        for p in processes:
            if p.arrival_time <= time and p.completion_time is None and p not in ready:
                ready.append(p)

        if not ready:
            # no ready processes: jump to next arrival
            future = [p.arrival_time for p in processes if p.completion_time is None and p.arrival_time > time]
            if not future:
                break
            time = min(future)
            continue

        # pick process with smallest burst time (then arrival_time, then pid)
        ready.sort(key=lambda x: (x.burst_time, x.arrival_time, x.pid))
        current = ready.pop(0)
        start = time
        # run to completion (tick-by-tick)
        for _ in range(current.burst_time):
            time += 1
        end = time
        current.completion_time = end
        completed += 1
        gantt.append({"pid": current.pid, "start": start, "end": end, "color": colors[current.pid]})

    gantt = _merge_segments(gantt)
    metrics, averages = _finalize_metrics(processes)
    return gantt, metrics, averages


def srtf_preemptive(process_list: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, float]]:
    """
    Shortest Remaining Time First (preemptive SJF).
    Simulates tick-by-tick and can preempt the running process when a shorter-job arrives.
    """
    processes = [Process(**p) for p in process_list]
    colors = _assign_colors([p.pid for p in processes])
    time = 0
    n = len(processes)
    completed = 0
    gantt = []
    last_pid = None

    while completed < n:
        # select arrived processes with remaining > 0
        arrived = [p for p in processes if p.arrival_time <= time and p.remaining > 0]
        if not arrived:
            # idle until next arrival
            futures = [p.arrival_time for p in processes if p.remaining > 0 and p.arrival_time > time]
            if not futures:
                break
            time = min(futures)
            continue

        # pick process with smallest remaining time (tie-break arrival_time, pid)
        arrived.sort(key=lambda x: (x.remaining, x.arrival_time, x.pid))
        current = arrived[0]

        # execute one tick
        if last_pid is None or last_pid != current.pid:
            gantt.append({"pid": current.pid, "start": time, "end": time + 1, "color": colors[current.pid]})
        else:
            gantt[-1]["end"] = time + 1

        current.remaining -= 1
        time += 1

        if current.remaining == 0:
            current.completion_time = time
            completed += 1

        last_pid = current.pid

    gantt = _merge_segments(gantt)
    metrics, averages = _finalize_metrics(processes)
    return gantt, metrics, averages


def round_robin(process_list: List[Dict[str, Any]], quantum: int) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, float]]:
    """
    Round Robin scheduling with given time quantum.
    Simulated tick-by-tick: each process runs up to 'quantum' ticks (or less if it finishes),
    arrivals are enqueued as time advances.
    """
    if quantum <= 0:
        raise ValueError("Quantum must be > 0 for Round Robin")

    processes = [Process(**p) for p in process_list]
    colors = _assign_colors([p.pid for p in processes])
    time = 0
    n = len(processes)
    gantt = []
    ready_queue: List[Process] = []
    completed = 0

    # Sort arrivals and iterate
    arrival_events = sorted(processes, key=lambda x: (x.arrival_time, x.pid))
    arrival_iter = iter(arrival_events)
    next_arrival = next(arrival_iter, None)

    def enqueue_arrivals(up_to_time):
        nonlocal next_arrival
        while next_arrival and next_arrival.arrival_time <= up_to_time:
            if next_arrival.remaining > 0 and next_arrival not in ready_queue:
                ready_queue.append(next_arrival)
            next_arrival = next(arrival_iter, None)

    # initial enqueue at time 0
    enqueue_arrivals(0)

    while completed < n:
        if not ready_queue:
            # idle until next arrival
            if next_arrival:
                time = max(time, next_arrival.arrival_time)
                enqueue_arrivals(time)
                if not ready_queue:
                    continue
            else:
                break

        current = ready_queue.pop(0)
        ticks = 0
        # execute up to quantum ticks
        while ticks < quantum and current.remaining > 0:
            # add/extend gantt segment
            if gantt and gantt[-1]["pid"] == current.pid and gantt[-1]["end"] == time:
                gantt[-1]["end"] = time + 1
            else:
                gantt.append({"pid": current.pid, "start": time, "end": time + 1, "color": colors[current.pid]})
            current.remaining -= 1
            time += 1
            ticks += 1
            # enqueue arrivals that occurred at this time
            enqueue_arrivals(time)

        if current.remaining == 0:
            current.completion_time = time
            completed += 1
        else:
            # ensure arrivals at this time are enqueued before re-adding current to queue
            enqueue_arrivals(time)
            ready_queue.append(current)

    gantt = _merge_segments(gantt)
    metrics, averages = _finalize_metrics(processes)
    return gantt, metrics, averages


# Public registry mapping string names to functions
ALGORITHM_REGISTRY = {
    "FCFS": fcfs,
    "SJF": sjf_non_preemptive,
    "SRTF": srtf_preemptive,
    "RR": round_robin
}
