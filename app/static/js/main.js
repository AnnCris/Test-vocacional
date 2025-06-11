// Funcionalidad para el gráfico radar en la página de resultados
function initializeResultsChart() {
    const chartElement = document.getElementById('resultsChart');
    if (!chartElement) return;
    
    // El gráfico se inicializa en el bloque de scripts de results.html
}

// Funcionalidad para la barra de navegación responsive
document.addEventListener('DOMContentLoaded', function() {
    // Cerrar el menú desplegable al hacer clic en un enlace
    const navLinks = document.querySelectorAll('.nav-link');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            // Solo colapsar en dispositivos móviles
            if (window.innerWidth < 992) {
                navbarCollapse.classList.remove('show');
            }
        });
    });
    
    // Inicializar gráficos si están en la página
    initializeResultsChart();
});

// Validación de formulario de registro
document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.querySelector('form[action*="register"]');
    if (!registerForm) return;
    
    registerForm.addEventListener('submit', function(event) {
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm_password').value;
        
        if (password !== confirmPassword) {
            event.preventDefault();
            alert('Las contraseñas no coinciden');
        }
    });
});

// Validación para el formulario de perfil (notas académicas)
document.addEventListener('DOMContentLoaded', function() {
    const profileForm = document.querySelector('form[action*="profile"]');
    if (!profileForm) return;
    
    const scoreInputs = [
        document.getElementById('math_score'),
        document.getElementById('science_score'),
        document.getElementById('language_score'),
        document.getElementById('social_science_score'),
        document.getElementById('arts_score')
    ];
    
    scoreInputs.forEach(input => {
        if (!input) return;
        
        input.addEventListener('change', function() {
            const value = parseFloat(this.value);
            if (value < 1) this.value = 1;
            if (value > 10) this.value = 10;
        });
    });
});