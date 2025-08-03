document.addEventListener('DOMContentLoaded', function() {
    const html = document.documentElement;
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = themeToggle.querySelector('i');
    const navbar = document.querySelector('.dynamic-navbar');
    const passwordFields = document.querySelectorAll('input[type="password"]');
    let lastScrollTop = 0;
    
    const currentTheme = html.getAttribute('data-theme') || 'light';
    updateIcon(currentTheme);

    themeToggle.addEventListener('click', function() {
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateIcon(newTheme);
    });

    function updateIcon(theme) {
        if (theme === 'dark') {
            themeIcon.classList.replace('bi-moon-fill', 'bi-sun-fill');
            themeToggle.title = 'Switch to Light Mode';
        } else {
            themeIcon.classList.replace('bi-sun-fill', 'bi-moon-fill');
            themeToggle.title = 'Switch to Dark Mode';
        }
    }

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
        lastScrollTop = currentScroll <= 0 ? 0 : currentScroll;
    });

    passwordFields.forEach(field => {
        const wrapper = document.createElement('div');
        wrapper.className = 'input-group';
        field.parentNode.insertBefore(wrapper, field);
        wrapper.appendChild(field);

        const toggle = document.createElement('span');
        toggle.className = 'input-group-text';
        toggle.innerHTML = '<i class="bi bi-eye"></i>';
        wrapper.appendChild(toggle);

        toggle.addEventListener('click', function() {
            const isPassword = field.type === 'password';
            field.type = isPassword ? 'text' : 'password';
            toggle.innerHTML = `<i class="bi bi-${isPassword ? 'eye-slash' : 'eye'}"></i>`;
        });    
    });
});