// API URL (actualiza si es necesario)
const API_URL = 'http://localhost:5000/api/sensor_data';

// Función para obtener los datos de la API y llenar la tabla
async function fetchSensorData() {
    try {
        const response = await fetch(API_URL);
        const result = await response.json();

        // Verifica si los datos están dentro de "data"
        if (result.data && Array.isArray(result.data)) {
            populateTable(result.data); // Llama a populateTable si los datos son válidos
        } else {
            console.error('Formato de respuesta inesperado:', result);
        }
    } catch (error) {
        console.error('Error al obtener los datos del sensor:', error);
    }
}

// Función para llenar la tabla con los datos
function populateTable(data) {
    const tableBody = document.getElementById('data-table').querySelector('tbody');
    tableBody.innerHTML = ''; // Limpia las filas existentes

    data.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${item.id}</td>
            <td>${item.fecha}</td>
            <td>${item.hora}</td>
            <td>${item.idsensor}</td>
            <td>${item.valor+" ºC"}</td>
        `;
        tableBody.appendChild(row); // Agrega la fila a la tabla
    });
}

// Función para aplicar los filtros a la tabla
function applyFilters() {
    const idFilter = document.getElementById('filter-id').value.toLowerCase();
    const dateFilter = document.getElementById('filter-date').value;
    const timeFilter = document.getElementById('filter-time').value;
    const valueFilter = document.getElementById('filter-value').value;

    const rows = document.querySelectorAll('#data-table tbody tr');
    rows.forEach(row => {
        const [id, date, time, sensorId,value] = row.children;

        // Filtra por ID, Fecha y Hora
        const matchesId = !idFilter || sensorId.textContent.toLowerCase().includes(idFilter);
        const matchesDate = !dateFilter || date.textContent === dateFilter;
        const matchesTime = !timeFilter || time.textContent.startsWith(timeFilter);
        const matchValue = !valueFilter|| value.textContent == valueFilter;

        if (matchesId && matchesDate && matchesTime && matchValue) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// Función para restablecer los filtros
function resetFilters() {
    document.getElementById('filter-id').value = '';
    document.getElementById('filter-date').value = '';
    document.getElementById('filter-time').value = '';
    applyFilters(); // Reaplica los filtros para mostrar todas las filas
}

// Obtener y mostrar los datos cuando la página se carga
window.onload = fetchSensorData;