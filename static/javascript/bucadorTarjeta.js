document.getElementById('buscador').addEventListener('input', function() {
    let query = this.value;

    // Limpia la sección de resultados si el input está vacío o tiene menos de 5 caracteres
    let informacionProducto = document.getElementById('informacion_producto');
    informacionProducto.innerHTML = '';

    if (query.length < 6) {
        // Si el input tiene menos de 5 caracteres, no hace la búsqueda y limpia los resultados
        return;
    }
    
    // Realiza la solicitud AJAX cuando el query tiene al menos 5 caracteres
    fetch(`/buscar?nombre=${query}`)
    .then(response => response.json())
    .then(data => {
        // Limpia la sección de resultados nuevamente antes de actualizarla con nuevos datos
        informacionProducto.innerHTML = '';

        // Iterar sobre los resultados y actualizarlos en la interfaz
        data.forEach(producto => {
            let div = document.createElement('div');
            div.classList.add('primer_info'); 
            div.innerHTML = `
                <p>Tarjeta: <span>${producto.tarjeta}</span></p>
                <p>Nombre: <span>${producto.nombre}</span></p>
                <p>Color: <span>${producto.color}</span></p>
                <p>Seccion: <span>${producto.seccion}</span></p>
                <p>Tip. Producto: <span>${producto.tip_prod}</span></p>
                <p>Tipo Produccion: <span>${producto.tipo_produccion}</span></p>
                <p>Fecha: <span>${producto.fecha}</span></p>
                <p>Hojas: <span>${producto.hojas}</span></p>
                <p>Calibre: <span>${producto.calibre}</span></p>
                <p>Cliente: <span>${producto.cliente}</span></p>
            `;
            informacionProducto.appendChild(div);
        });
    });
});