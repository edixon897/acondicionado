document.getElementById('loginForm').addEventListener('submit', function(event){
    event.preventDefault(); 

    const nombre = document.getElementById('nombre').value;
    const contrasena = document.getElementById('contraseña').value;
    const mensajeDiv = document.getElementById('mensaje');

    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/login', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

    xhr.onreadystatechange = function() {
        if(xhr.readyState === XMLHttpRequest.DONE) {
            const response = JSON.parse(xhr.responseText);

            if(response.success) {
                mensajeDiv.textContent = response.message;
                mensajeDiv.classList.remove('error');
                mensajeDiv.classList.add('success');
                window.location.href = response.redirect_url; 
            } else {
                mensajeDiv.textContent = response.error;
                mensajeDiv.classList.remove('success');
                mensajeDiv.classList.add('error');
            }
        }
    };

    xhr.send(`nombre=${encodeURIComponent(nombre)}&contraseña=${encodeURIComponent(contrasena)}`);
});
