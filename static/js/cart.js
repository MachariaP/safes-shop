// static/js/cart.js
document.addEventListener('DOMContentLoaded', () => {
    const cartBadge = document.getElementById('cartBadge');
    const quantityInputs = document.querySelectorAll('.quantity-input');
    const removeButtons = document.querySelectorAll('.btn-remove');

    // Function to get cart from localStorage or initialize empty
    function getCart() {
        return JSON.parse(localStorage.getItem('cart')) || {};
    }

    // Function to save cart to localStorage and update badge
    function saveCart(cart) {
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartBadge();
        syncCartWithServer(cart);
    }

    // Function to update cart badge
    function updateCartBadge() {
        const cart = getCart();
        const itemCount = Object.keys(cart).length;
        if (cartBadge) {
            cartBadge.textContent = itemCount;
        }
        // Dispatch custom event for base.html
        window.dispatchEvent(new Event('cartUpdated'));
    }

    // Function to sync cart with server
    function syncCartWithServer(cart) {
        fetch('{% url "store:update_cart" %}', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({ cart }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status !== 'success') {
                console.error('Failed to sync cart:', data.message);
            }
        })
        .catch(error => console.error('Error syncing cart:', error));
    }

    // Function to get CSRF token
    function getCSRFToken() {
        const name = 'csrftoken';
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [key, value] = cookie.trim().split('=');
            if (key === name) return value;
        }
        return '';
    }

    // Handle quantity changes
    quantityInputs.forEach(input => {
        input.addEventListener('change', (e) => {
            const slug = e.target.dataset.slug;
            const quantity = parseInt(e.target.value);
            if (quantity < 1) {
                e.target.value = 1;
                return;
            }
            const cart = getCart();
            if (cart[slug]) {
                cart[slug].quantity = quantity;
                saveCart(cart);
                // Refresh page to update totals
                window.location.reload();
            }
        });
    });

    // Handle remove item
    removeButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const slug = e.target.closest('.btn-remove').dataset.slug;
            const cart = getCart();
            delete cart[slug];
            saveCart(cart);
            // Refresh page to update cart
            window.location.reload();
        });
    });

    // Initial badge update
    updateCartBadge();
});
