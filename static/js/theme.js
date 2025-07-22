// Added for dark mode toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    const html = document.documentElement;
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = themeToggle.querySelector('i');

    // Set initial icon based on current theme (set by inline script in main.html)
    const currentTheme = html.getAttribute('data-theme') || 'light';
    updateIcon(currentTheme);

    // Toggle theme on button click
    themeToggle.addEventListener('click', function() {
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateIcon(newTheme);
    });

    // Update icon based on theme
    function updateIcon(theme) {
        if (theme === 'dark') {
            themeIcon.classList.replace('bi-sun-fill', 'bi-moon-fill');
            themeToggle.title = 'Switch to Light Mode';
        } else {
            themeIcon.classList.replace('bi-moon-fill', 'bi-sun-fill');
            themeToggle.title = 'Switch to Dark Mode';
        }
    }
});