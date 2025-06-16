// static/js/cart.js
document.addEventListener('DOMContentLoaded', () => {
    const cartBadge = document.getElementById('cartBadge');
    const cartTableBody = document.querySelector('.cart-table tbody');
    const cartSummary = document.querySelector('.cart-summary');
    const emptyCartMessage = document.querySelector('.empty-cart');
    let isFetching = false; // Prevent multiple simultaneous fetches

    function getCSRFToken() {
        const name = 'csrftoken';
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [key, value] = cookie.trim().split('=');
            if (key === name) return value;
        }
        return '';
    }

    // Debounce function to limit fetchCart calls
    function debounce(func, wait) {
        let timeout;
        return function (...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }

    // Fetch and update cart content
    async function fetchCart() {
        if (isFetching) return; // Skip if already fetching
        isFetching = true;
        try {
            const response = await fetch('/store/cart/', {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
            });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            const data = await response.json();
            if (data.status === 'success') {
                console.log('Fetched server cart:', data);
                if (cartTableBody && cartSummary) {
                    // Update cart table
                    const itemsHtml = data.cart_items.map(item => `
                        <tr>
                            <td>
                                <div class="d-flex align-items-center">
                                    <img src="${item.image}" alt="${item.product.name}" class="cart-item-img me-3">
                                    <span>${item.product.name}</span>
                                </div>
                            </td>
                            <td>Ksh ${item.price.toFixed(2)}</td>
                            <td>
                                <input type="number" class="form-control quantity-input" data-slug="${item.product.slug}" value="${item.quantity}" min="1">
                            </td>
                            <td>Ksh ${item.total.toFixed(2)}</td>
                            <td>
                                <button class="btn btn-remove" data-slug="${item.product.slug}">
                                    <i class="fas fa-trash-alt"></i>
                                </button>
                            </td>
                        </tr>
                    `).join('');
                    cartTableBody.innerHTML = itemsHtml || '';

                    // Update cart summary
                    cartSummary.innerHTML = `
                        <h4>Cart Summary</h4>
                        <hr>
                        <p><strong>Total Items:</strong> ${data.cart_count}</p>
                        <p><strong>Total Price:</strong> Ksh ${data.total_price.toFixed(2)}</p>
                        <a href="${window.storeUrls.checkout}" class="btn btn-checkout w-100">Proceed to Checkout</a>
                        <a href="${window.storeUrls.productList}" class="btn-continue-shopping w-100 mt-2">Continue Shopping</a>
                    `;

                    // Show/hide empty cart message
                    if (emptyCartMessage) {
                        emptyCartMessage.style.display = data.cart_items.length ? 'none' : 'block';
                    }

                    // Rebind event listeners
                    bindEventListeners();
                }
                window.dispatchEvent(new Event('cartUpdated')); // Trigger badge update
            }
        } catch (error) {
            console.error('Error fetching cart:', error);
        } finally {
            isFetching = false;
        }
    }

    // Sync cart changes with server
    async function syncCartWithServer(slug, quantity) {
        try {
            const response = await fetch('/store/update-cart/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: JSON.stringify({ cart: { [slug]: { quantity, price: null } } }), // Price validated server-side
            });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            const data = await response.json();
            if (data.status === 'success') {
                console.log('Cart synced successfully');
                fetchCart(); // Refresh cart view
            } else {
                console.warn('Cart sync failed:', data.message);
            }
        } catch (error) {
            console.error('Error syncing cart:', error);
        }
    }

    // Remove item from cart
    async function removeItem(slug) {
        try {
            const response = await fetch('/store/update-cart/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: JSON.stringify({ cart: {} }), // Empty cart for removal
            });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            const data = await response.json();
            if (data.status === 'success') {
                console.log('Item removed successfully');
                fetchCart(); // Refresh cart view
            }
        } catch (error) {
            console.error('Error removing item:', error);
        }
    }

    // Bind event listeners for quantity inputs and remove buttons
    function bindEventListeners() {
        const quantityInputs = document.querySelectorAll('.quantity-input');
        const removeButtons = document.querySelectorAll('.btn-remove');

        quantityInputs.forEach(input => {
            input.removeEventListener('change', handleQuantityChange); // Prevent duplicate listeners
            input.addEventListener('change', handleQuantityChange);
        });

        removeButtons.forEach(button => {
            button.removeEventListener('click', handleRemoveClick); // Prevent duplicate listeners
            button.addEventListener('click', handleRemoveClick);
        });
    }

    // Handlers for quantity and remove events
    const handleQuantityChange = async (e) => {
        const slug = e.target.dataset.slug;
        const quantity = parseInt(e.target.value);
        if (quantity < 1) {
            e.target.value = 1;
            return;
        }
        await syncCartWithServer(slug, quantity);
    };

    const handleRemoveClick = async (e) => {
        const slug = e.target.closest('.btn-remove').dataset.slug;
        await removeItem(slug);
    };

    // Debounced fetchCart to prevent excessive calls
    const debouncedFetchCart = debounce(fetchCart, 300);

    // Initial cart fetch
    debouncedFetchCart();
});
