import matplotlib

matplotlib.use("Agg")

import networkx as nx

import matplotlib.pyplot as plt

import uuid  # Add this import to generate unique filenames

import os  # Add this import to delete files


def visualize_cpm_graph(tasks, critical_path=None): # Wizualizacja Grafu CPM Activity on Arrow

    G = nx.DiGraph()


    for task in tasks:

        G.add_node(task["name"], duration=float(task["duration"]))

        if task["dependencies"] != "-":

            for dep in task["dependencies"].split(','):

                G.add_edge(dep.strip(), task["name"])

    pos = nx.spring_layout(G)


    plt.figure(figsize=(12, 6))

    plt.gca().set_facecolor('black')

    nx.draw(G, pos, with_labels=False, node_color='green', edge_color='white', node_size=2000)


    node_labels = {n: G.nodes[n]['duration'] for n in G.nodes()}

    nx.draw_networkx_labels(G, pos, labels=node_labels, font_color='white', font_size=12)


    edge_labels = {}

    for task in tasks:

        if task["dependencies"] != "-":

            for dep in task["dependencies"].split(','):

                edge_labels[(dep.strip(), task["name"])] = task["name"]


    nx.draw_networkx_edge_labels(

        G,

        pos,

        edge_labels=edge_labels,

        font_color='violet',

        font_size=20,

        label_pos=0.6,

        bbox=dict(alpha=0),

        verticalalignment='bottom'  # Add this argument
        
    )


    if critical_path:

        crit_edges = list(zip(critical_path, critical_path[1:]))

        nx.draw_networkx_edges(G, pos, edgelist=crit_edges, width=3, edge_color='yellow', arrows=True, arrowstyle='-|>', arrowsize=20)


    plt.title("Graf CPM (Activity on Arrow)", color='white')

    filename = f"cpm_graph_aoa_{uuid.uuid4()}.png"  # Generate a unique filename

    plt.savefig(filename, facecolor='black')

    plt.close()

    plt.clf()  # Clear the figure

    return filename


def visualize_cpm_graph_aon(tasks, critical_path=None):

    G = nx.DiGraph()


    for task in tasks:

        G.add_node(task["name"], duration=float(task["duration"]))

        if task["dependencies"] != "-":

            for dep in task["dependencies"].split(','):

                G.add_edge(dep.strip(), task["name"])

    pos = nx.spring_layout(G)


    plt.figure(figsize=(12, 6))

    plt.gca().set_facecolor('black')

    nx.draw(G, pos, with_labels=True, node_shape='s', node_color='red', edge_color='white', node_size=2000, font_size=10, font_color='white')


    if critical_path:

        crit_edges = list(zip(critical_path, critical_path[1:]))
        
        nx.draw_networkx_edges(G, pos, edgelist=crit_edges, width=3, edge_color='yellow', arrows=True, arrowstyle='-|>', arrowsize=20)


    plt.title("Graf CPM (Activity on Node)", color='white')

    filename = f"cpm_graph_aon_{uuid.uuid4()}.png"  # Generate a unique filename

    plt.savefig(filename, facecolor='black')

    plt.close()

    plt.clf()  # Clear the figure

    return filename

def delete_temp_files(filenames):

    for filename in filenames:

        try:

            if os.path.exists(filename):

                os.remove(filename)

        except PermissionError:
            
            print(f"PermissionError: Could not delete {filename}. It might be in use.")