// static/js/base.js

document.addEventListener('DOMContentLoaded', () => {
    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        });
    }

    // Newsletter form validation and feedback
    const newsletterForm = document.querySelector('footer form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const emailInput = newsletterForm.querySelector('input[type="email"]');
            if (emailInput && !isValidEmail(emailInput.value)) {
                emailInput.classList.add('is-invalid');
                emailInput.focus();
                alert('Please enter a valid email address.');
            } else if (emailInput) {
                newsletterForm.submit(); // Submit to Django view
                emailInput.classList.remove('is-invalid');
                alert('Thank you! You’ve subscribed successfully.');
                newsletterForm.reset();
            }
        });
    }

    // Close dropdowns when clicking outside
    document.addEventListener('click', (e) => {
        const dropdowns = document.querySelectorAll('.dropdown-menu');
        if (dropdowns) {
            dropdowns.forEach(dropdown => {
                if (!dropdown.parentElement.contains(e.target)) {
                    dropdown.classList.remove('show');
                }
            });
        }
    });

    // Helper function for email validation
    function isValidEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
});