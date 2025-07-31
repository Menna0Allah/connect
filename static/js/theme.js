// static/js/theme.js
document.addEventListener('DOMContentLoaded', function() {
    const html = document.documentElement;
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = themeToggle.querySelector('i');
    const navbar = document.querySelector('.dynamic-navbar');
    let lastScrollTop = 0;

    // Set initial icon based on current theme
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
            themeIcon.classList.replace('bi-moon-fill', 'bi-sun-fill');
            themeToggle.title = 'Switch to Light Mode';
        } else {
            themeIcon.classList.replace('bi-sun-fill', 'bi-moon-fill');
            themeToggle.title = 'Switch to Dark Mode';
        }
    }

    // Navbar scroll behavior
    window.addEventListener('scroll', function() {
        let currentScroll = window.pageYOffset || document.documentElement.scrollTop;

        if (currentScroll > lastScrollTop) {
            // Scrolling down
            navbar.classList.remove('visible');
            navbar.classList.add('hidden');
        } else {
            // Scrolling up
            navbar.classList.remove('hidden');
            navbar.classList.add('visible');
        }
        lastScrollTop = currentScroll <= 0 ? 0 : currentScroll; // Prevent negative scroll values
    });

    // Updated: Match Recent Activity section height to Rooms section without scrolling
    function matchActivityHeight() {
        const roomsSection = document.getElementById('rooms-section');
        const activitySection = document.getElementById('activity-section');
        if (roomsSection && activitySection) {
            activitySection.style.height = 'auto'; // Reset height
            const roomsHeight = roomsSection.offsetHeight;
            // Set height to 95% of Rooms section to account for padding/margins
            activitySection.style.height = `${Math.floor(roomsHeight * 0.95)}px`;
            activitySection.style.overflow = 'hidden'; // Prevent scrolling
        }
    }

    // Run on load and resize
    matchActivityHeight();
    window.addEventListener('resize', matchActivityHeight);
});