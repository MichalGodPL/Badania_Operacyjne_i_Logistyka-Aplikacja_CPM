from CPMLiczenie import calculate_cpm

def calculate_cpm_predecessor(tasks):
    graph = {t["name"]: [] for t in tasks}
    in_degree = {t["name"]: 0 for t in tasks}
    durations = {}
    for t in tasks:
        durations[t["name"]] = t["duration"]
        for dep in t["dependencies"]:
            if dep != "-":
                graph[dep].append(t["name"])
                in_degree[t["name"]] += 1

    queue = [n for n, d in in_degree.items() if d == 0]
    earliest_start = {t["name"]: 0 for t in tasks}
    earliest_finish = {}

    while queue:
        current = queue.pop(0)
        earliest_finish[current] = earliest_start[current] + durations[current]
        for neighbor in graph[current]:
            earliest_start[neighbor] = max(earliest_start[neighbor], earliest_finish[current])
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    total_duration = max(earliest_finish.values()) if earliest_finish else 0
    critical_path = get_critical_path(earliest_start, earliest_finish, durations)
    result = calculate_cpm(tasks)
    return result

def get_critical_path(earliest_start, earliest_finish, durations):
    critical_path = []
    for task, finish_time in earliest_finish.items():
        if finish_time == max(earliest_finish.values()):
            critical_path.append({"name": task, "duration": durations[task]})
    return critical_path
