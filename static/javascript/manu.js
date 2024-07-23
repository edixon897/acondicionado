function toggleMenu() {
    const menuOptions = document.getElementById('menu-options');
    menuOptions.style.display = menuOptions.style.display === 'none' || menuOptions.style.display === '' ? 'block' : 'none';

    
 /*    window.addEventListener('click', (event) => {
        if (event.target === menuOptions) {
            modal.style.display = 'none';
        }
    }); */
}


// Close menu when clicking outside the menu-content
window.onclick = function(event) {
    const menuOptions = document.getElementById('menu-options');
    const menuContent = document.querySelector('.menu-options .menu-content');
    if (event.target === menuOptions && !menuContent.contains(event.target)) {
        menuOptions.style.display = 'none';
    }

}

document.addEventListener('DOMContentLoaded', function() {
    const rows = document.querySelectorAll('#tabla_productos tbody tr');

    rows.forEach(row => {
        row.addEventListener('click', function() {
            this.classList.toggle('expanded');
        });
    });
});
    

/* BUSCADOR EN TIEMPO REAL PAGINA DE INICIO */


document.addEventListener('DOMContentLoaded', (event) => {
    let currentPage = 1;
    let perPage = 10;

    const modal = document.getElementById('modal');
    const modalContent = document.getElementById('modal-body');
    const closeModal = document.querySelector('#modal .close');

    // Guardar el contenido original de la tabla
    const tableBody = document.querySelector('#tabla_productos tbody');
    const originalTableContent = tableBody.innerHTML;

    async function searchItems(page = 1) {
        // Obtener los valores de búsqueda
        let nameValue = document.getElementById('buscador').value;
        let colorValue = document.getElementById('buscador-color').value;
        let caliberValue = document.getElementById('buscador-calibre').value;
        let clientValue = document.getElementById('seleccion-cliente').value;
        let sessionValue = document.getElementById('seleccion-sesion').value;
        let tipoProdValue = document.getElementById('tipo-producto').value;

        // Comprobar si todos los valores están vacíos
        if (!nameValue && !colorValue && !caliberValue && !clientValue && !sessionValue && !tipoProdValue) {
            // Restaurar el contenido original de la tabla si no hay búsqueda
            tableBody.innerHTML = originalTableContent;
            attachEventListeners();
             // Recargar la página para restablecer el estado inicial
            location.reload();
            return;
        }

        let formData = new FormData();
        formData.append('name', nameValue);
        formData.append('color', colorValue);
        formData.append('caliber', caliberValue);
        formData.append('client', clientValue);
        formData.append('session', sessionValue);
        formData.append('tipo_prod', tipoProdValue);
        formData.append('page', page);
        formData.append('per_page', perPage);

        let response = await fetch('/filtrar_busqueda', {
            method: 'POST',
            body: formData
        });

        let result = await response.json();

        if (result.error) {
            console.error(result.error);
            return;
        }

        let data = result.data;
        let totalCount = result.total_count;

        tableBody.innerHTML = ''; // Limpiar la tabla solo si hay búsqueda

        data.forEach(item => {
            let formattedDate = new Date(item[6]).toISOString().split('T')[0];
            let row = document.createElement('tr');
            row.innerHTML = `
                <td>${item[0]}</td>
                <td>${item[1]} </td>
                <td>${item[3]}</td>
                 <td class="ver-mas-cell">
                    <button class="ver-mas-btn">
                        <img class="ver-mas" src="/static/img/vista.png" alt="Ver más">
                    </button>
                 </td>
                <td data-label="color">${item[2]}</td>
                <td data-label="Calibre">${item[8]}</td>
                <td data-label="Tip. Produ">${item[4]}</td>
                <td data-label="Familia">${item[5]}</td>
                <td data-label="Fecha">${formattedDate}</td>
                <td data-label="Hojas">${item[7]}</td>
            `;
            tableBody.appendChild(row);
        });

        attachEventListeners();
    }


    function attachEventListeners() {
        console.log('Asignando event listeners a los botones "ver más"');
        document.querySelectorAll('.ver-mas-btn').forEach((button) => {
            button.addEventListener('click', (event) => {
                // Obtener los datos de la fila clickeada
                const row = event.target.closest('tr');
                const rowData = Array.from(row.children).map(cell => cell.textContent.trim());

                // Rellenar el modal con los datos de la fila
                modalContent.innerHTML = `
                    <p><strong>Tarjeta:</strong> ${rowData[0]}</p>
                    <p><strong>Nombre de producto:</strong> ${rowData[1]}</p>
                    <p><strong>Sección:</strong> ${rowData[2]}</p>
                    <p><strong>Color:</strong> ${rowData[4]}</p>
                    <p><strong>Calibre:</strong> ${rowData[5]}</p>
                    <p><strong>Tip. Produ:</strong> ${rowData[6]}</p>
                    <p><strong>Familia:</strong> ${rowData[7]}</p>
                    <p><strong>Fecha:</strong> ${rowData[8]}</p>
                    <p><strong>Hojas:</strong> ${rowData[9]}</p>
                `;

                // Mostrar el modal
                modal.style.display = 'block';
            });
        });
    }

    // Cerrar el modal cuando se hace click en la "X"
    closeModal.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    // Cerrar el modal cuando se hace click fuera del contenido del modal
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    

    // Add event listeners to trigger search only when there is input or change
    document.getElementById('buscador').addEventListener('input', () => searchItems(currentPage));
    document.getElementById('buscador-color').addEventListener('input', () => searchItems(currentPage));
    document.getElementById('buscador-calibre').addEventListener('input', () => searchItems(currentPage));
    document.getElementById('seleccion-cliente').addEventListener('change', () => searchItems(currentPage));
    document.getElementById('seleccion-sesion').addEventListener('change', () => searchItems(currentPage));
    document.getElementById('tipo-producto').addEventListener('change', () => searchItems(currentPage));

    

    
    attachEventListeners();
});
