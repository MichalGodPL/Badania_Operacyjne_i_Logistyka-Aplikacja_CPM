import webview

import os

from CPMLiczenie import calculate_cpm

from CPMGrafy import visualize_cpm_graph, visualize_cpm_graph_aon

from CPMGantt import visualize_gantt_chart


class API:

    def __init__(self):

        self.tasks = []


    def add_task(self, tasks):

        for task in tasks:

            self.tasks.append({

                "name": task["name"],

                "duration": float(task["duration"]),

                "dependencies": [dep for dep in task["dependencies"].split(",") if dep != "-"]

            })

        return {"message": "Zadania zostały zapisane"}


    def save_csv_to_desktop(self, csv_content):

        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

        file_path = os.path.join(desktop_path, "tasks.csv")

        with open(file_path, "w", encoding="utf-8") as f:

            f.write(csv_content)

        return {"message": f"Plik CSV zapisany na pulpicie: {file_path}"}


    def calculate_cpm(self, tasks):

        result = calculate_cpm(tasks)

        return result


    def visualize_cpm_graph(self, tasks, critical_path=None):

        graph_path = visualize_cpm_graph(tasks, critical_path)

        return {"message": "Graf CPM (Activity on Arrow) został wygenerowany", "graph_path": graph_path}


    def visualize_cpm_graph_aon(self, tasks, critical_path=None):

        graph_path = visualize_cpm_graph_aon(tasks, critical_path)

        return {"message": "Graf CPM (Activity on Node) został wygenerowany", "graph_path": graph_path}
    

    def visualize_gantt_chart(self, tasks):

        graph_path = visualize_gantt_chart(tasks)

        return {"message": "Wykres Gantta został wygenerowany", "graph_path": graph_path}

    def delete_temp_files(self, filenames):
        from CPMGrafy import delete_temp_files
        delete_temp_files(filenames)

api = API()


# Pobranie pełnej ścieżki do pliku Index.html

html_path = os.path.abspath("Index.html")

url = f"file:///{html_path}"


# Tworzenie okna PyWebview i uruchamianie aplikacji

webview.create_window("Metoda CPM", url, js_api=api, width=1600, height=900)

webview.start()