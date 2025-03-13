def calculate_cpm(tasks):
    graph = {t["name"]: [] for t in tasks}
    in_degree = {t["name"]: 0 for t in tasks}
    durations = {}
    for t in tasks:
        durations[t["name"]] = float(t["duration"])  # Ensure duration is a float
        for dep in t["dependencies"].split(','):  # Split dependencies by comma
            if dep.strip() != "-":
                graph[dep.strip()].append(t["name"])
                in_degree[t["name"]] += 1

    queue = [n for n, d in in_degree.items() if d == 0]
    earliest_start = {t["name"]: 0 for t in tasks}
    earliest_finish = {}

    calculations = []
    while queue:
        current = queue.pop(0)
        earliest_finish[current] = earliest_start[current] + durations[current]
        for neighbor in graph[current]:
            earliest_start[neighbor] = max(earliest_start[neighbor], earliest_finish[current])
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
        calculations.append({
            "task": current,
            "earliest_start": earliest_start[current],
            "earliest_finish": earliest_finish[current],
            "latest_start": None,  # Placeholder for now
            "latest_finish": None  # Placeholder for now
        })

    total_duration = max(earliest_finish.values()) if earliest_finish else 0
    critical_path = get_critical_path(earliest_start, earliest_finish, durations)

    # Calculate latest start and finish times
    latest_finish = {task: total_duration for task in earliest_finish}
    latest_start = {task: total_duration - durations[task] for task in earliest_finish}

    for task in reversed(list(earliest_finish.keys())):
        for neighbor in graph[task]:
            latest_finish[task] = min(latest_finish[task], latest_start[neighbor])
        latest_start[task] = latest_finish[task] - durations[task]

    for calc in calculations:
        calc["latest_start"] = latest_start[calc["task"]]
        calc["latest_finish"] = latest_finish[calc["task"]]

    return {"message": f"Szacowany czas realizacji (CPM): {total_duration}", "path": critical_path, "calculations": calculations}

def get_critical_path(earliest_start, earliest_finish, durations):
    critical_path = []
    for task, finish_time in earliest_finish.items():
        if finish_time == max(earliest_finish.values()):
            critical_path.append({"name": task, "duration": durations[task]})
    return critical_path
