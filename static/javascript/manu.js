function toggleMenu() {
    const menuOptions = document.getElementById('menu-options');
    menuOptions.style.display = menuOptions.style.display === 'none' || menuOptions.style.display === '' ? 'block' : 'none';

 /*    window.onclick = function(event) {
        const menuOptions = document.getElementById('menu-options');
        const menuContent = document.querySelector('.menu-options .menu-content');
        if (event.target === menuOptions && !menuContent.contains(event.target)) {
            menuOptions.style.display = 'none';
        }
    
    }
 */
    
 
}



/* document.addEventListener('DOMContentLoaded', function() {
    const rows = document.querySelectorAll('#tabla_productos tbody tr');

    rows.forEach(row => {
        row.addEventListener('click', function() {
            this.classList.toggle('expanded');
        });
    });
});

window.addEventListener('click', (event) => {
    const menuOptions = document.getElementById('menu-options');
    if (event.target === menuOptions) {
        menuOptions.style.display = 'none';
    }
}); 


 */
