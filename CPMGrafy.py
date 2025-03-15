import matplotlib
matplotlib.use("Agg")
import networkx as nx
import matplotlib.pyplot as plt

def visualize_cpm_graph(tasks):
    G = nx.DiGraph()
    for task in tasks:
        G.add_node(task["name"], duration=float(task["duration"]))
        if task["dependencies"] != "-":
            for dep in task["dependencies"].split(','):
                G.add_edge(dep.strip(), task["name"])
    
    pos = nx.planar_layout(G)
    plt.figure(figsize=(12, 6))
    nx.draw(G, pos, with_labels=True, node_color='green', edge_color='black', node_size=2000, font_size=10)
    plt.title("Graf CPM (Activity on Arrow)")
    plt.savefig("cpm_graph_aoa.png")
    plt.close()
    return "cpm_graph_aoa.png"

def visualize_cpm_graph_aon(tasks):
    G = nx.DiGraph()
    for task in tasks:
        G.add_node(task["name"], duration=float(task["duration"]))
        if task["dependencies"] != "-":
            for dep in task["dependencies"].split(','):
                G.add_edge(dep.strip(), task["name"])
    
    pos = nx.spring_layout(G)  # Replace graphviz_layout
    plt.figure(figsize=(12, 6))
    nx.draw(G, pos, with_labels=True, node_shape='s', node_color='red', edge_color='black', node_size=2000, font_size=10)
    plt.title("Graf CPM (Activity on Node)")
    plt.savefig("cpm_graph_aon.png")
    plt.close()
    return "cpm_graph_aon.png"
