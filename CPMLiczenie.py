import matplotlib.pyplot as plt

def calculate_cpm(tasks):
    """
    Oblicza pełne parametry metody CPM dla metody poprzedników
    """
    graph = {t["name"]: [] for t in tasks}
    in_degree = {t["name"]: 0 for t in tasks}
    durations = {t["name"]: float(t["duration"]) for t in tasks}
    
    for t in tasks:
        for dep in t["dependencies"].split(','):
            dep = dep.strip()
            if dep != "-":
                graph[dep].append(t["name"])
                in_degree[t["name"]] += 1
    
    # Krok do przodu (Forward Pass)
    queue = [n for n, d in in_degree.items() if d == 0]
    earliest_start = {t["name"]: 0 for t in tasks}
    earliest_finish = {}
    
    while queue:
        current = queue.pop(0)
        earliest_finish[current] = earliest_start[current] + durations[current]
        for neighbor in graph[current]:
            earliest_start[neighbor] = max(earliest_start.get(neighbor, 0), earliest_finish[current])
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if not earliest_start:
        return {"message": "Brak danych do obliczenia CPM", "critical_path": [], "calculations": []}
    
    total_duration = max(earliest_finish.values())
    
    # Krok do tyłu (Backward Pass)
    latest_finish = {task: total_duration for task in earliest_finish}
    latest_start = {task: total_duration - durations[task] for task in earliest_finish}
    
    for task in reversed(list(earliest_finish.keys())):
        for neighbor in graph[task]:
            latest_finish[task] = min(latest_finish[task], latest_start[neighbor])
        latest_start[task] = latest_finish[task] - durations[task]
    
    # Obliczanie rezerw czasowych
    total_floats = {task: latest_start[task] - earliest_start[task] for task in earliest_start}
    
    # Wyznaczanie ścieżki krytycznej
    critical_path = [task for task, r in total_floats.items() if r == 0]
    
    calculations = []
    for task in earliest_finish:
        calculations.append({
            "task": task,
            "earliest_start": earliest_start[task],
            "earliest_finish": earliest_finish[task],
            "latest_start": latest_start[task],
            "latest_finish": latest_finish[task],
            "total_float": latest_finish[task] - earliest_finish[task],
            "free_float": latest_start[task] - earliest_start[task]
        })
    
    return {
        "message": f"Szacowany czas realizacji (CPM): {max(earliest_finish.values())}",
        "critical_path": critical_path,
        "calculations": calculations
    }

def visualize_cpm_graph(tasks):
    """
    Wizualizuje graf CPM jako diagram zależności AON bez użycia NetworkX
    """
    plt.figure(figsize=(10, 6))
    
    node_positions = {}
    for i, task in enumerate(tasks):
        node_positions[task["name"]] = (i * 2, 5)  # Rozmieszczenie węzłów
        plt.text(i * 2, 5, task["name"], fontsize=12, ha='center', va='center', bbox=dict(facecolor='lightblue', edgecolor='black'))
    
    for task in tasks:
        for dep in task["dependencies"].split(','):
            dep = dep.strip()
            if dep != "-":
                x1, y1 = node_positions[dep]
                x2, y2 = node_positions[task["name"]]
                plt.plot([x1, x2], [y1, y2], 'k-', lw=2)  # Rysowanie krawędzi
    
    plt.xlim(-1, len(tasks) * 2)
    plt.ylim(4, 6)
    plt.axis('off')
    plt.title("Graf CPM - Model AON")
    plt.show()

def visualize_gantt_chart(tasks, earliest_start):
    """
    Tworzy wykres Gantta dla harmonogramu ASAP
    """
    plt.figure(figsize=(10, 6))
    yticks = []
    ylabels = []
    for i, task in enumerate(tasks):
        plt.barh(i, task["duration"], left=earliest_start[task["name"]], color='skyblue')
        yticks.append(i)
        ylabels.append(task["name"])
    
    plt.yticks(yticks, ylabels)
    plt.xlabel("Czas")
    plt.ylabel("Zadania")
    plt.title("Wykres Gantta - Harmonogram ASAP")
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.show()