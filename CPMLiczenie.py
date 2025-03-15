import networkx as nx

import matplotlib.pyplot as plt


def calculate_cpm(tasks):

    G = nx.DiGraph()

    durations = {}
    

    for task in tasks:

        G.add_node(task["name"], duration=float(task["duration"]))

        durations[task["name"]] = float(task["duration"])
        

        if task["dependencies"] != "-":

            for dep in task["dependencies"].split(','):

                G.add_edge(dep.strip(), task["name"])
    

    earliest_start = {node: 0 for node in G.nodes}

    for node in nx.topological_sort(G):

        earliest_start[node] = max((earliest_start[pre] + durations[pre]) for pre in G.predecessors(node)) if G.in_edges(node) else 0
    

    earliest_finish = {node: earliest_start[node] + durations[node] for node in G.nodes}

    total_duration = max(earliest_finish.values())

    latest_finish = {node: total_duration for node in G.nodes}
    

    for node in reversed(list(nx.topological_sort(G))):

        latest_finish[node] = min((latest_finish[succ] - durations[succ]) for succ in G.successors(node)) if G.out_edges(node) else total_duration
    

    latest_start = {node: latest_finish[node] - durations[node] for node in G.nodes}

    total_floats = {node: latest_start[node] - earliest_start[node] for node in G.nodes}

    critical_path = [node for node, tf in total_floats.items() if tf == 0]
    

    calculations = [{

        "task": node,

        "earliest_start": earliest_start[node],

        "earliest_finish": earliest_finish[node],

        "latest_start": latest_start[node],

        "latest_finish": latest_finish[node],

        "total_float": total_floats[node]

    } for node in G.nodes]

    
    return {

        "message": f"Szacowany czas realizacji (CPM): {total_duration}",
        
        "critical_path": critical_path,

        "calculations": calculations

    }