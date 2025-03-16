import matplotlib.pyplot as plt

import pandas as pd

import matplotlib.dates as mdates


def visualize_gantt_chart(tasks):

    df = pd.DataFrame(tasks)

    df['start'] = df['earliest_start']

    df['end'] = df['start'] + df['duration']


    fig, ax = plt.subplots(figsize=(12, 6), facecolor='black')

    ax.set_facecolor('black')

    for spine in ax.spines.values():

        spine.set_color('white')

    ax.tick_params(axis='x', colors='white')

    ax.tick_params(axis='y', colors='white')

    ax.set_xlabel('Czas (dni)', color='white')

    ax.set_ylabel('Zadania', color='white')

    ax.set_title('Wykres Gantta', color='white')

    ax.grid(True, color='white', linestyle='--', alpha=0.3)


    for idx, row in df.iterrows():

        ax.barh(row['name'], row['duration'], left=row['start'], color='skyblue')


    plt.gca().invert_yaxis()

    plt.savefig("gantt_chart.png", facecolor='black')

    plt.close()

    plt.clf() 
    
    return "gantt_chart.png"