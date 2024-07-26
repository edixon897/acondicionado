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


document.addEventListener('DOMContentLoaded', function () {
    const buscador = document.getElementById('buscador');
    const suggestions = document.getElementById('suggestions');
    const tablaBody = document.getElementById('tabla_body');
    const originalTableContent = tablaBody.innerHTML; 

    buscador.addEventListener('input', function () {
        const query = buscador.value;

        if (query.length > 0) {
            fetch(`/buscar_color?color=${query}`)
                .then(response => response.json())
                .then(data => {
                    suggestions.innerHTML = '';
                    data.suggestions.forEach(suggestion => {
                        const div = document.createElement('div');
                        div.classList.add('suggestion-item');
                        div.textContent = suggestion;
                        suggestions.appendChild(div);
                    });

                    tablaBody.innerHTML = '';
                    data.results.forEach(row => {
                        const tr = document.createElement('tr');
                        tr.innerHTML = `
                            <td>${row.color}</td>
                            <td>${row.seccion}</td>
                            <td data-label="Hojas">${row.total_hojas}</td>
                        `;
                        tablaBody.appendChild(tr);
                    });
                })
                .catch(error => console.error('Error:', error));
        } else {
            suggestions.innerHTML = '';
            tablaBody.innerHTML = originalTableContent;
            location.reload();
            return;
        }
    });

    suggestions.addEventListener('click', function (e) {
        if (e.target.classList.contains('suggestion-item')) {
            buscador.value = e.target.textContent;
            suggestions.innerHTML = '';
            buscador.dispatchEvent(new Event('input'));
        }
    });
});
