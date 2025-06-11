// static/js/cart.js
document.addEventListener('DOMContentLoaded', () => {
    const cartBadge = document.getElementById('cartBadge');
    const quantityInputs = document.querySelectorAll('.quantity-input');
    const removeButtons = document.querySelectorAll('.btn-remove');

    function getCart() {
        return JSON.parse(localStorage.getItem('cart')) || {};
    }

    function saveCart(cart) {
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartBadge();
        syncCartWithServer(cart);
    }

    function updateCartBadge() {
        const cart = getCart();
        let itemCount = 0;
        for (const slug in cart) {
            itemCount += cart[slug].quantity;
        }
        if (cartBadge) {
            cartBadge.textContent = itemCount;
        }
        window.dispatchEvent(new Event('cartUpdated'));
    }

    function syncCartWithServer(cart) {
        fetch('/store/update-cart/', {
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
                console.error('Error syncing cart:', data.message);
            }
        })
        .catch(error => console.error('Error syncing cart:', error));
    }

    function getCSRFToken() {
        const name = 'csrftoken';
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [key, value] = cookie.trim().split('=');
            if (key === name) return value;
        }
        return '';
    }

    // Fetch server-side cart on page load to initialize localStorage
    fetch('/store/cart/', {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
    .then(response => response.json())
    .then(data => {
        let cart = getCart();
        data.cart_items.forEach(item => {
            cart[item.product.slug] = {
                quantity: item.quantity,
                price: item.price.toString(),
            };
        });
        saveCart(cart);
    })
    .catch(error => console.error('Error fetching cart:', error));

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
            window.location.reload();
        });
    });

    updateCartBadge();
});