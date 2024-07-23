function togglePassword(fieldId) {
    const field = document.getElementById(fieldId);
    const eye = document.querySelector(`#${fieldId} + span`);
    if (field.type === 'password') {
        field.type = 'text';
        eye.textContent = '🙈';
    } else {
        field.type = 'password';
        eye.textContent = '👁️';
    }
}

function toggleEyeIcon(fieldId, eyeId) {
    const field = document.getElementById(fieldId);
    const eye = document.getElementById(eyeId);
    if (field.value.length > 0) {
        eye.style.display = 'inline';
    } else {
        eye.style.display = 'none';
    }
}