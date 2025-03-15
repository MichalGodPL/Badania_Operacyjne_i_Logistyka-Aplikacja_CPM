import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

def visualize_gantt_chart(tasks):
    df = pd.DataFrame(tasks)
    df['start'] = pd.to_datetime(df['earliest_start'], unit='D')
    df['end'] = df['start'] + pd.to_timedelta(df['duration'], unit='D')

    fig, ax = plt.subplots(figsize=(12, 6))
    for idx, row in df.iterrows():
        ax.barh(row['name'], row['duration'], left=row['start'], color='skyblue')

    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().invert_yaxis()
    plt.xlabel('Czas')
    plt.ylabel('Zadania')
    plt.title('Wykres Gantta')
    plt.grid(True)
    plt.savefig("gantt_chart.png")
    plt.close()
    return "gantt_chart.png"
