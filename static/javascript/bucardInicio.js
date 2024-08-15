
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
       
        let clientValue = document.getElementById('seleccion-cliente').value;
        let sessionValue = document.getElementById('seleccion-sesion').value;
        let tipoProdValue = document.getElementById('tipo-producto').value;

        // Comprobar si todos los valores están vacíos
        if (!nameValue && !colorValue  && !clientValue && !sessionValue && !tipoProdValue) {
            tableBody.innerHTML = originalTableContent;
            attachEventListeners();
            /* location.reload(); */
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

        let result = await response.json();

        if (result.error) {
            console.error(result.error);
            return;
        }

        let data = result.data;

        tableBody.innerHTML = ''; 

        data.forEach(item => {
            let formattedDate = new Date(item[6]).toISOString().split('T')[0];
            let row = document.createElement('tr');
            row.innerHTML = `
                <td>${item[0]}</td>
                <td>${item[1]}, ${item[2]}, ${item[8]}</td>
                <td>${item[3]}</td>
                 <td class="ver-mas-cell">
                    <button class="ver-mas-btn">
                        <img class="ver-mas" src="/static/img/vista.png" alt="Ver más">
                    </button>
                 </td>
                <td data-label="Tip. Produ">${item[4]}</td>
                <td data-label="tipo_produccion">${item[5]}</td>
                <td data-label="cliente">${item[9]}</td>
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
                    <p><strong>Tip. Produ:</strong> ${rowData[4]}</p>
                    <p><strong>tipo_produccion:</strong> ${rowData[5]}</p>
                    <p><strong>Cliente:</strong> ${rowData[9]}</p>
                    <p><strong>Fecha:</strong> ${rowData[7]}</p>
                    <p><strong>Hojas:</strong> ${rowData[8]}</p>
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
                searchItems(); // Llama a la función de búsqueda que ya tienes definida
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


