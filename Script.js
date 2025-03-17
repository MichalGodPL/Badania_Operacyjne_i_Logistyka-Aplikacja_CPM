let currentCard = 1;

function showCard(cardNumber) {
    const current = document.getElementById(`card${currentCard}`);
    const next = document.getElementById(`card${cardNumber}`);
    current.classList.add('hidden');
    setTimeout(() => {
        current.style.display = 'none';
        next.style.display = 'block';
        setTimeout(() => {
            next.classList.remove('hidden');
        }, 10); // Small delay to trigger transition
    }, 300); // Match the transition duration
    currentCard = cardNumber;
}

function prevCard() {
    const nextCardNumber = currentCard === 1 ? 3 : currentCard - 1;
    showCard(nextCardNumber);
}

function nextCard() {
    const nextCardNumber = currentCard === 3 ? 1 : currentCard + 1;
    showCard(nextCardNumber);
}

function createTaskTable() {
    let rows = parseInt(document.getElementById('tableRows').value);
    let tableContainer = document.getElementById('tableContainer');
    tableContainer.innerHTML = "";
    
    let table = document.createElement('table');
    let thead = document.createElement('thead');
    let headerRow = document.createElement('tr');
    
    let th1 = document.createElement('th');
    th1.innerText = "Nazwa Czynności";
    let th2 = document.createElement('th');
    th2.innerText = "Czas Trwania";
    let th3 = document.createElement('th');
    th3.innerText = "Poprzednik";
    headerRow.append(th1, th2, th3);
    thead.appendChild(headerRow);
    table.appendChild(thead);
    
    let tbody = document.createElement('tbody');
    for (let i = 0; i < rows; i++) {
        let tr = document.createElement('tr');
        for (let j = 0; j < 3; j++) {
            let td = document.createElement('td');
            td.contentEditable = "true";

            // Dla "Czas Trwania" - tylko cyfry
            if (j === 1) {
                td.addEventListener('input', (e) => {
                    e.target.textContent = e.target.textContent.replace(/[^\d]/g, '');
                });
            }

            tr.appendChild(td);
        }
        tbody.appendChild(tr);
    }
    table.appendChild(tbody);
    tableContainer.appendChild(table);
}

function generateCPM() {
    let table = document.querySelector('#tableContainer table');
    if (!table) {
        alert("Brak tabeli do wygenerowania CPM.");
        return;
    }

    let tasks = [];
    let rows = table.querySelectorAll('tbody tr');
    rows.forEach(row => {
        let cells = row.querySelectorAll('td');
        tasks.push({
            name: cells[0].innerText,
            duration: cells[1].innerText,
            dependencies: cells[2].innerText
        });
    });

    // Call Python API to calculate CPM
    window.pywebview.api.calculate_cpm(tasks).then(response => {
        document.getElementById('cpmResult').innerText = response.message;
        const totalDuration = response.calculations.reduce((max, task) => Math.max(max, task.earliest_finish), 0);
        const earliestFinish = response.calculations.reduce((max, task) => Math.max(max, task.earliest_finish), 0);
        const latestFinish = response.calculations.reduce((max, task) => Math.max(max, task.latest_finish), 0);
        drawCPMChart(totalDuration, earliestFinish, latestFinish);
        generateCPMModel(response.critical_path);
        displayCalculations(response.calculations, response.critical_path);
        showCard(2); // Switch to the second card to display the result

        // Prepare tasks with earliest_start for Gantt chart
        let ganttTasks = response.calculations.map(calc => ({
            name: calc.task,
            duration: calc.earliest_finish - calc.earliest_start,
            earliest_start: calc.earliest_start
        }));

        // Call Python API to visualize CPM graph (Activity on Node)
        window.pywebview.api.visualize_cpm_graph_aon(tasks, response.critical_path).then(respAON => {
            let container = document.getElementById('cpmGraphContainer');
            container.innerHTML = `<img src="${respAON.graph_path}" style="width: 100%; border-radius: 15px; overflow: hidden;"/>`;

            // Call Python API to visualize CPM graph (Activity on Arrow)
            window.pywebview.api.visualize_cpm_graph(tasks, response.critical_path).then(respAOA => {
                container.innerHTML += `<img src="${respAOA.graph_path}" style="width: 100%; margin-top: 20px; border-radius: 15px; overflow: hidden;"/>`;

                // Call Python API to visualize the Gantt chart in the third card
                window.pywebview.api.visualize_gantt_chart(ganttTasks).then(respGantt => {
                    let ganttCardContainer = document.querySelector('#card3 #ganttChartContainer');
                    ganttCardContainer.innerHTML = `<img src="${respGantt.graph_path}" style="width: 100%; border-radius: 15px; overflow: hidden;"/>`;
                    // showCard(3); // Comment or remove this to avoid switching to card 3 automatically

                    // Delete temporary files
                    window.pywebview.api.delete_temp_files([respAON.graph_path, respAOA.graph_path, respGantt.graph_path]);
                }).catch(error => {
                    console.error("Error generating Gantt chart:", error);
                    alert("Wystąpił błąd podczas generowania wykresu Gantta.");
                });
            }).catch(error => {
                console.error("Error generating CPM graph (arrow):", error);
                alert("Wystąpił błąd podczas generowania grafu CPM (arrow).");
            });
        }).catch(error => {
            console.error("Error generating CPM graph (node):", error);
            alert("Wystąpił błąd podczas generowania grafu CPM (node).");
        });

        displayCriticalPath(response.critical_path); // Add this line
    }).catch(error => {
        console.error("Error generating CPM:", error);
        alert("Wystąpił błąd podczas generowania CPM.");
    });
}

function displayCriticalPath(criticalPath) {
    const container = document.getElementById('cpmModelContainer');
    container.innerHTML = `<div class="critical-path">Ścieżka Krytyczna: ${criticalPath.join(' → ')}</div>`;
}

function generateCPMModel(path) {
    const container = document.getElementById('cpmModelContainer');
    container.innerHTML = '';
}

function drawCPMChart(totalDuration, earliestFinish, latestFinish) {
    const ctx = document.getElementById('cpmChart').getContext('2d');
    const labels = ['Szacowane zakończenie modelu', 'Najwcześniejsze zakończenie', 'Najpóźniejsze zakończenie'];
    const data = [totalDuration, earliestFinish, latestFinish];

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Czas trwania',
                data: data,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function displayCalculations(calculations, criticalPath) {
    const container = document.getElementById('cpmCalculationsContainer');
    container.innerHTML = '';

    let table = document.createElement('table');
    let thead = document.createElement('thead');
    let headerRow = document.createElement('tr');

    let headers = [
        "Zadanie",
        "Najwcześniejszy Start",
        "Najwcześniejsze Zakończenie",
        "Najpóźniejszy Start",
        "Najpóźniejsze Zakończenie",
        "Rezerwa Czasu",
        "Czy ŚK?"
    ];
    headers.forEach(header => {
        let th = document.createElement('th');
        th.innerText = header;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    let tbody = document.createElement('tbody');
    calculations.forEach(calc => {
        let tr = document.createElement('tr');
        let tdTask = document.createElement('td');
        tdTask.innerText = calc.task;
        let tdES = document.createElement('td');
        tdES.innerText = calc.earliest_start;
        let tdEF = document.createElement('td');
        tdEF.innerText = calc.earliest_finish;
        let tdLS = document.createElement('td');
        tdLS.innerText = calc.latest_start;
        let tdLF = document.createElement('td');
        tdLF.innerText = calc.latest_finish;
        let tdSlack = document.createElement('td');
        tdSlack.innerText = calc.latest_finish - calc.earliest_finish;
        let tdIsCritical = document.createElement('td');
        tdIsCritical.innerText = criticalPath.includes(calc.task) ? "Tak" : "Nie";
        tr.append(tdTask, tdES, tdEF, tdLS, tdLF, tdSlack, tdIsCritical);
        tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    container.appendChild(table);
}

function exportToCSV() {
    let table = document.querySelector('#tableContainer table');
    if (!table) {
        alert("Brak tabeli do eksportowania.");
        return;
    }

    let csvContent = "";
    let rows = table.querySelectorAll('tbody tr'); // Select only tbody rows to exclude headers
    rows.forEach(row => {
        let cells = row.querySelectorAll('td');
        let rowContent = Array.from(cells).map(cell => cell.innerText.trim()).join(",");
        csvContent += rowContent + "\n"; // Użycie \n zamiast \r\n dla lepszej zgodności
    });

    let encodedUri = "data:text/csv;charset=utf-8," + encodeURIComponent(csvContent);
    let link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "tasks.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    // Save CSV to desktop using Python API
    window.pywebview.api.save_csv_to_desktop(csvContent).then(response => {
        alert(response.message);
    }).catch(error => {
        console.error("Error exporting CSV:", error);
        alert("Wystąpił błąd podczas eksportowania do CSV.");
    });
}

function uploadCSV(event) {
    const file = event.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = function(e) {
        const csvContent = e.target.result;
        const rows = csvContent
            .split('\n')
            .map(line => line.trim())
            .filter(line => line !== '')
            .map(line => line.split(','));
        let tableContainer = document.getElementById('tableContainer');
        tableContainer.innerHTML = "";

        let table = document.createElement('table');
        let thead = document.createElement('thead');
        let headerRow = document.createElement('tr');

        let th1 = document.createElement('th');
        th1.innerText = "Nazwa Czynności";
        let th2 = document.createElement('th');
        th2.innerText = "Czas Trwania";
        let th3 = document.createElement('th');
        th3.innerText = "Poprzednik";
        headerRow.append(th1, th2, th3);
        thead.appendChild(headerRow);
        table.appendChild(thead);

        let tbody = document.createElement('tbody');
        rows.forEach(row => {
            let tr = document.createElement('tr');
            for (let i = 0; i < 3; i++) {
                let td = document.createElement('td');
                td.contentEditable = "true";
                if (i === 1) {
                    td.addEventListener('input', (e) => {
                        e.target.textContent = e.target.textContent.replace(/[^\d]/g, '');
                    });
                }
                td.innerText = row[i] ? row[i].trim() : "";
                tr.appendChild(td);
            }
            tbody.appendChild(tr);
        });
        table.appendChild(tbody);
        tableContainer.appendChild(table);
    };
    reader.readAsText(file);
}

document.addEventListener('keydown', function(event) {
    if (event.key === 'ArrowLeft') {
        prevCard();
    } else if (event.key === 'ArrowRight') {
        nextCard();
    }
});
