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

    def calculate_cpm(self, tasks):
        method = tasks[0]["dependencies"].find("-") != -1
        if method:
            from cpm_successor import calculate_cpm_successor
            result = calculate_cpm_successor(tasks)
        else:
            from cpm_predecessor import calculate_cpm_predecessor
            result = calculate_cpm_predecessor(tasks)
        return result

api = API()

html_path = os.path.abspath("Index.html")
css_path = os.path.abspath("styles.css")
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read().replace('styles.css', f"file:///{css_path}")

# Tworzenie okna PyWebview i uruchamianie aplikacji
webview.create_window("Metoda CPM", html=html_content, js_api=api, width=900, height=500)
webview.start()