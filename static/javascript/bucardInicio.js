document.addEventListener('DOMContentLoaded', (event) => {
    let currentPage = 1;
    let perPage = 10000;

    const modal = document.getElementById('modal');
    const modalContent = document.getElementById('modal-body');
    const closeModal = document.querySelector('#modal .close');

    const tableBody = document.querySelector('#datos-tabla');
    const originalTableContent = tableBody.innerHTML;

    async function searchItems(page = 1) {
        let nameValue = document.getElementById('buscador').value;
        let colorValue = document.getElementById('buscador-color').value;
        let clientValue = document.getElementById('seleccion-cliente').value;
        let sessionValue = document.getElementById('seleccion-sesion').value;
        let tipoProdValue = document.getElementById('tipo-producto').value;

        if (!nameValue && !colorValue && !clientValue && !sessionValue && !tipoProdValue) {
            tableBody.innerHTML = originalTableContent;
            attachEventListeners();
            return;
        }

        let formData = new FormData();
        formData.append('name', nameValue);
        formData.append('color', colorValue);
        formData.append('client', clientValue);
        formData.append('session', sessionValue);
        formData.append('tipo_prod', tipoProdValue);
        formData.append('page', page);
        formData.append('per_page', perPage);

        let response = await fetch('/filtrar_busqueda', {
            method: 'POST',
            body: formData
        });

        // Verificación de errores en la respuesta
        if (!response.ok) {
            console.error(`Error: ${response.status} ${response.statusText}`);
            return;
        }

        let result = await response.json();

        if (result.error) {
            console.error(result.error);
            return;
        }

        let data = result.data;

        tableBody.innerHTML = '';

        data.forEach(item => {
            let row = document.createElement('tr');

            if (item[0] === null) {
                if (item[1] !== null) {
                    row.classList.add('total-row');
                    row.innerHTML = `<td colspan="9">${item[1]}: ${item[7]}</td>`;
                } else if (item[2] !== null && item[3] === null) {
                    row.classList.add('total-row');
                    row.innerHTML = `<td colspan="9">${item[2]}: ${item[7]}</td>`;
                } else if (item[3] !== null && item[2] === null) {
                    row.classList.add('total-row');
                    row.innerHTML = `<td colspan="9">${item[3]}: ${item[7]}</td>`;
                }
            } else {
                let formattedDate = new Date(item[6]).toISOString().split('T')[0];
                row.innerHTML = `
                    <td>${item[0]}</td>
                    <td>${item[1]} ${item[2]} ${item[8]}</td>
                    <td>${item[3]}</td>
                    <td data-label="Tip. Produ">${item[4]}</td>
                    <td data-label="tipo_produccion">${item[5]}</td>
                    <td data-label="cliente">${item[9]}</td>
                    <td data-label="Fecha">${formattedDate}</td>
                    <td data-label="Hojas">${item[7]}</td>
                     <td class="ver-mas-cell">
                        <button class="ver-mas-btn">
                            <img class="ver-mas" src="/static/img/vista.png" alt="Ver más">
                        </button>
                    </td>
                `;
            }

            tableBody.appendChild(row);
        });

        attachEventListeners();
    }

    function attachEventListeners() {
        document.querySelectorAll('.ver-mas-btn').forEach((button) => {
            button.addEventListener('click', (event) => {
                const row = event.target.closest('tr');
                const rowData = Array.from(row.children).map(cell => cell.textContent.trim());

                modalContent.innerHTML = `
                    <p><strong>Tarjeta:</strong> ${rowData[0]}</p>
                    <p><strong>Nombre de producto:</strong> ${rowData[1]}</p>
                    <p><strong>Sección:</strong> ${rowData[2]}</p>
                    <p><strong>Tip. Produ:</strong> ${rowData[3]}</p>
                    <p><strong>tipo_produccion:</strong> ${rowData[4]}</p>
                    <p><strong>Cliente:</strong> ${rowData[5]}</p>
                    <p><strong>Fecha:</strong> ${rowData[6]}</p>
                    <p><strong>Hojas:</strong> ${rowData[7]}</p>
                `;

                modal.style.display = 'block';
            });
        });
    }

    closeModal.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    document.getElementById('buscador').addEventListener('input', () => searchItems(currentPage));
    document.getElementById('buscador-color').addEventListener('input', () => searchItems(currentPage));
    document.getElementById('seleccion-cliente').addEventListener('change', () => searchItems(currentPage));
    document.getElementById('seleccion-sesion').addEventListener('change', () => searchItems(currentPage));
    document.getElementById('tipo-producto').addEventListener('change', () => searchItems(currentPage));

    attachEventListeners();
});




document.addEventListener('DOMContentLoaded', function() {
        const buscadorInput = document.getElementById('buscador');
        const suggestionsBox = document.getElementById('suggestions');

        buscadorInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            let items = suggestionsBox.querySelectorAll('.suggestion-item');
            
            let hasSuggestions = false;
            items.forEach(item => {
                if (item.textContent.toLowerCase().includes(searchTerm)) {
                    item.style.display = 'block';
                    hasSuggestions = true;
                } else {
                    item.style.display = 'none';
                }
            });

            suggestionsBox.style.display = hasSuggestions ? 'block' : 'none';
        });

        suggestionsBox.addEventListener('click', function(event) {
            if (event.target.classList.contains('suggestion-item')) {
                buscadorInput.value = event.target.textContent;
                suggestionsBox.style.display = 'none';
                searchItems(); 
            }
        });

        document.addEventListener('click', function(event) {
            if (!event.target.closest('.buscador') && event.target !== buscadorInput) {
                suggestionsBox.style.display = 'none';
            }
        });


        function searchItems() {
            const searchValue = buscadorInput.value;
            console.log('Buscar con:', searchValue);
            
        }
    });




        document.addEventListener('DOMContentLoaded', function() {
            const buscardorcolor = document.getElementById('buscador-color');
            const suggestionsB = document.getElementById('suggestion');

            buscardorcolor.addEventListener('input', function() {
                const searchTerm = this.value.toLowerCase();
                let items = suggestionsB.querySelectorAll('.suggestion-itemm');
                
                items.forEach(item => {
                    if (item.textContent.toLowerCase().includes(searchTerm)) {
                        item.style.display = 'block';
                    } else {
                        item.style.display = 'none';
                    }
                });

                suggestionsB.style.display = searchTerm ? 'block' : 'none';
            });

            suggestionsB.addEventListener('click', function(event) {
                if (event.target.classList.contains('suggestion-itemm')) {
                    buscardorcolor.value = event.target.textContent;
                    suggestionsB.style.display = 'none';
                }
            });

            document.addEventListener('click', function(event) {
                if (!event.target.closest('.buscador-color')) {
                    suggestionsB.style.display = 'none';
                }
            });
        });


