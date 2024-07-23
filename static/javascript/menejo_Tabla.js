document.addEventListener("DOMContentLoaded", function () {
    const rowsPerPage = 10;
    let currentPage = 1;

    const table = document.querySelector("#tabla_productos tbody");
    const rows = Array.from(table.querySelectorAll("tr"));
    const totalRows = rows.length;
    const totalPages = Math.ceil(totalRows / rowsPerPage);

    const resultsCountContainer = document.querySelector(".results-count");
    resultsCountContainer.innerText = `Total resultados: ${totalRows}`;

    const paginationContainer = document.querySelector(".paginacion");
    const pageIndicator = paginationContainer.querySelector("#pagina-actual");
    const nextButton = paginationContainer.querySelector("#siguiente");
    const prevButton = paginationContainer.querySelector("#anterior");

    function renderTable(page) {
        table.innerHTML = "";

        const start = (page - 1) * rowsPerPage;
        const end = start + rowsPerPage;

        const rowsToDisplay = rows.slice(start, end);
        rowsToDisplay.forEach(row => table.appendChild(row));

        pageIndicator.innerText = page;
    }

    function updatePaginationButtons() {
        nextButton.disabled = currentPage === totalPages;
        prevButton.disabled = currentPage === 1;
    }

    nextButton.addEventListener("click", function () {
        if (currentPage < totalPages) {
            currentPage++;
            renderTable(currentPage);
            updatePaginationButtons();
        }
    });

    prevButton.addEventListener("click", function () {
        if (currentPage > 1) {
            currentPage--;
            renderTable(currentPage);
            updatePaginationButtons();
        }
    });

    renderTable(currentPage);
    updatePaginationButtons();
});



/*   document.addEventListener('DOMContentLoaded', function () {
    const toggleButton = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    const currentTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', currentTheme);

    if (currentTheme === 'dark') {
      themeIcon.classList.remove('fa-moon');
      themeIcon.classList.add('fa-sun');
    }

    toggleButton.addEventListener('click', function () {
      let theme = document.documentElement.getAttribute('data-theme');
      if (theme === 'light') {
        document.documentElement.setAttribute('data-theme', 'dark');
        themeIcon.classList.remove('fa-moon');
        themeIcon.classList.add('fa-sun');
        localStorage.setItem('theme', 'dark');
      } else {
        document.documentElement.setAttribute('data-theme', 'light');
        themeIcon.classList.remove('fa-sun');
        themeIcon.classList.add('fa-moon');
        localStorage.setItem('theme', 'light');
      }
    });
  });

 */