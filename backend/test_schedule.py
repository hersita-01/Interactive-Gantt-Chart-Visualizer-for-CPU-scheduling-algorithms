from scheduling_logic import ALGORITHM_REGISTRY

SAMPLES = [
    ("Simple sequential", [
        {"pid": "P1", "arrival_time": 0, "burst_time": 3},
        {"pid": "P2", "arrival_time": 1, "burst_time": 2},
    ]),
    ("Overlap preemptive", [
        {"pid": "P1", "arrival_time": 0, "burst_time": 5},
        {"pid": "P2", "arrival_time": 2, "burst_time": 2},
        {"pid": "P3", "arrival_time": 3, "burst_time": 1},
    ]),
    ("Round robin", [
        {"pid": "A", "arrival_time": 0, "burst_time": 4},
        {"pid": "B", "arrival_time": 1, "burst_time": 3},
        {"pid": "C", "arrival_time": 2, "burst_time": 1},
    ]),
]


def run_all():
    for title, procs in SAMPLES:
        print('\n==== SAMPLE:', title, '====')
        for name, func in ALGORITHM_REGISTRY.items():
            try:
                if name == 'RR':
                    gantt, metrics, averages = func(procs, 2)
                else:
                    gantt, metrics, averages = func(procs)
                print(f'--- {name} ---')
                print('GANTT:')
                for seg in gantt:
                    print(f"  {seg}")
                print('METRICS:')
                for m in metrics:
                    print(f"  {m}")
                print('AVERAGES:', averages)
            except Exception as e:
                print(f'Error running {name}:', e)


if __name__ == '__main__':
    run_all()
