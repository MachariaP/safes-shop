// static/js/base.js
// Handles DOM-ready initialization and interactive features for the Diplomat Safes website

document.addEventListener('DOMContentLoaded', () => {
    // Navbar scroll effect: Adds shadow on scroll past 50px
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            navbar.classList.toggle('navbar-scrolled', window.scrollY > 50);
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

    // Cart badge update functionality
    function updateCartBadge() {
        const cart = JSON.parse(localStorage.getItem('cart')) || {};
        const cartBadge = document.getElementById('cartBadge');
        let itemCount = 0;

        for (const slug in cart) {
            itemCount += cart[slug].quantity || 0; // Default to 0 if quantity is undefined
        }

        if (cartBadge) {
            cartBadge.textContent = itemCount;
        }
    }

    // Initialize cart badge on page load
    updateCartBadge();

    // Listen for cart update events from other scripts
    window.addEventListener('cartUpdated', updateCartBadge);

    // Clear cart and update badge after order confirmation
    if (window.location.pathname.includes('/store/order-confirmation/')) {
        localStorage.removeItem('cart');
        updateCartBadge();
    }

    // Helper function to validate email format
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Helper function to retrieve CSRF token from cookies
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
