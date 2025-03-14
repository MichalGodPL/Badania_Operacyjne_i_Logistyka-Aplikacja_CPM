import matplotlib
matplotlib.use("Agg")
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

def visualize_cpm_graph(tasks):
    G = nx.DiGraph()
    for task in tasks:
        G.add_node(task["name"], duration=float(task["duration"]))
        if task["dependencies"] != "-":
            for dep in task["dependencies"].split(','):
                G.add_edge(dep.strip(), task["name"])
    
    pos = nx.spring_layout(G)  # Replace graphviz_layout
    plt.figure(figsize=(12, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='black', node_size=2000, font_size=10)
    plt.title("Graf CPM")
    plt.savefig("cpm_graph.png")
    plt.close()
    return "cpm_graph.png"

# def visualize_gantt_chart(tasks, earliest_start):
#     import plotly.express as px
#     import pandas as pd

#     df = pd.DataFrame(tasks)
#     df['duration'] = df['duration'].astype(float)
#     df['Start'] = df['name'].map(earliest_start).astype(float)
#     df['Finish'] = df['Start'] + df['duration']

#     print("Gantt chart data:", df.to_dict(orient='records'))  # Debug log

#     fig = px.timeline(df, x_start="Start", x_end="Finish", y="name", title="Wykres Gantta")
#     fig.update_yaxes(categoryorder="total ascending")
#     fig.update_layout(xaxis_type='linear', xaxis_range=[0, max(1, df['Finish'].max())])
#     # fig.write_html("gantt_chart.html")  # Removed - no file creation
#     # Removed return "gantt_chart.html"
#     return None
