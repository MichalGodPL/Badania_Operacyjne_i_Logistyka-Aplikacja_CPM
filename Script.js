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
        }, 10);
    }, 500);
    currentCard = cardNumber;
}

function prevCard() {
    const nextCardNumber = currentCard === 1 ? 2 : 1;
    showCard(nextCardNumber);
}

function nextCard() {
    const nextCardNumber = currentCard === 2 ? 1 : 2;
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

function saveTable() {
    let table = document.querySelector('#tableContainer table');
    if (!table) {
        alert("Brak tabeli do zapisania.");
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

    window.pywebview.api.add_task(tasks).then(response => {
        alert(response.message);
    }).catch(error => {
        console.error("Error saving tasks:", error);
    });
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

    window.pywebview.api.calculate_cpm(tasks).then(response => {
        document.getElementById('cpmResult').innerText = response.message;
        drawCPMChart(response.critical_path);
        generateCPMModel(response.critical_path);
        displayCalculations(response.calculations);
        showCard(2);
    }).catch(error => {
        console.error("Error generating CPM:", error);
    });
}

function exportToCSV() {
    let table = document.querySelector('#tableContainer table');
    if (!table) {
        alert("Brak tabeli do eksportowania.");
        return;
    }

    let csvContent = "data:text/csv;charset=utf-8,";
    let rows = table.querySelectorAll('tr');
    rows.forEach(row => {
        let cells = row.querySelectorAll('th, td');
        let rowContent = Array.from(cells).map(cell => cell.innerText).join(",");
        csvContent += rowContent + "\r\n";
    });

    let encodedUri = encodeURI(csvContent);
    let link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "tasks.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    window.pywebview.api.save_csv_to_desktop(csvContent).then(response => {
        alert(response.message);
    }).catch(error => {
        console.error("Error exporting CSV:", error);
    });
}

document.addEventListener('keydown', function(event) {
    if (event.key === 'ArrowLeft') {
        prevCard();
    } else if (event.key === 'ArrowRight') {
        nextCard();
    }
});
