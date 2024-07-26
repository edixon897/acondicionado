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