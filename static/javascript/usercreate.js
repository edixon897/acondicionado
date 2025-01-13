document.getElementById('formUser').addEventListener('submit', function(event) {
    event.preventDefault(); // Evita el comportamiento predeterminado del formulario
    const contrasena2 = document.getElementById('contrasena').value;
    const contrasena3 = document.getElementById('contrasena2').value;
    const mensaje = document.getElementById('mensajei');
    const nombre = document.getElementById('nombre').value;
    const apellido = document.getElementById('apellido').value;

    // Validar contraseñas antes de enviar al back end
    if (contrasena2 !== contrasena3) {
        mensaje.textContent = "Las contraseñas no coinciden.";
        mensaje.classList.remove('success');
        mensaje.classList.add('error');
        return; // No enviar solicitud si hay algun  error
    }

    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/agregarUsuario', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            const response = JSON.parse(xhr.responseText);
            if (response.success) {
                mensaje.textContent = response.message;
                mensaje.classList.remove('error');
                mensaje.classList.add('success');
                setTimeout(() => {
                    window.location.href = response.redirect_url;
                }, 30); // Redirige después de un pequeño retraso de 30 que equivale a 0.5 minutos
            } else {
                mensaje.textContent = response.message;
                mensaje.classList.remove('success');
                mensaje.classList.add('error');
            }
        }
    };

    xhr.send(`contrasena=${encodeURIComponent(contrasena2)}&contrasena2=${encodeURIComponent(contrasena3)}&nombre=${encodeURIComponent(nombre)}&apellido=${encodeURIComponent(apellido)}`);
});
