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

    // Update cart badge
    function updateCartBadge() {
        const cart = JSON.parse(localStorage.getItem('cart')) || {};
        const cartBadge = document.getElementById('cartBadge');
        let itemCount = 0;
        for (const slug in cart) {
            itemCount += cart[slug].quantity;
        }
        if (cartBadge) {
            cartBadge.textContent = itemCount;
        }
    }

    // Initial badge update
    updateCartBadge();

    // Listen for cart updates from other scripts
    window.addEventListener('cartUpdated', updateCartBadge);

    // Clear localStorage after checkout
    if (window.location.pathname.includes('/store/order-confirmation/')) {
        localStorage.removeItem('cart');
        updateCartBadge();
    }

    // Helper function for email validation
    function isValidEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    // Helper function to get CSRF token
    function getCSRFToken() {
        const name = 'csrftoken';
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [key, value] = cookie.trim().split('=');
            if (key === name) return value;
        }
        return '';
    }
});