import webview
import json
import os

class API:
    def __init__(self):
        self.tasks = []  # Miejsce do przechowywania wprowadzonych zadań

    def add_task(self, tasks):
        for task in tasks:
            self.tasks.append({
                "name": task["name"],
                "duration": float(task["duration"]),
                "dependencies": task["dependencies"].split(",") if task["dependencies"] else []
            })
        return {"message": "Zadania zostały zapisane"}

    def save_csv_to_desktop(self, csv_content):
        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        file_path = os.path.join(desktop_path, "tasks.csv")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(csv_content)
        return {"message": f"Plik CSV zapisany na pulpicie: {file_path}"}

    def calculate_cpm(self):
        # Przykładowa implementacja obliczeń metody CPM
        graph = {t["name"]: [] for t in self.tasks}
        in_degree = {t["name"]: 0 for t in self.tasks}
        durations = {}
        for t in self.tasks:
            durations[t["name"]] = t["duration"]
            for dep in t["dependencies"]:
                graph[dep].append(t["name"])
                in_degree[t["name"]] += 1

        queue = [n for n, d in in_degree.items() if d == 0]
        earliest_start = {t["name"]: 0 for t in self.tasks}
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
        return {"message": f"Szacowany czas realizacji (CPM): {total_duration}"}

api = API()

html_path = os.path.abspath("Index.html")
css_path = os.path.abspath("styles.css")
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read().replace('styles.css', f"file:///{css_path}")

# Tworzenie okna PyWebview i uruchamianie aplikacji
webview.create_window("Metoda CPM", html=html_content, js_api=api, width=900, height=500)
webview.start()