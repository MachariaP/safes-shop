document.addEventListener('DOMContentLoaded', () => {
    // Helper Functions
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function debounce(func, wait) {
        let timeout;
        return function (...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }

    // Quantity Control
    const decreaseQty = document.getElementById('decreaseQty');
    const increaseQty = document.getElementById('increaseQty');
    const qtyInput = document.getElementById('productQty');

    if (decreaseQty && increaseQty && qtyInput) {
        const updateQuantity = () => {
            let value = parseInt(qtyInput.value) || 1;
            if (value < 1) qtyInput.value = 1;
            else if (value > 10) qtyInput.value = 10;
        };

        decreaseQty.addEventListener('click', () => {
            let value = parseInt(qtyInput.value) - 1;
            qtyInput.value = value >= 1 ? value : 1;
        });

        increaseQty.addEventListener('click', () => {
            let value = parseInt(qtyInput.value) + 1;
            qtyInput.value = value <= 10 ? value : 10;
        });

        qtyInput.addEventListener('input', debounce(updateQuantity, 300));
    } else {
        console.warn('Quantity control elements not found');
    }

    // Image Gallery
    const galleryThumbs = document.querySelectorAll('.gallery-thumb');
    const mainImage = document.getElementById('mainProductImage');

    if (galleryThumbs.length && mainImage) {
        galleryThumbs.forEach(thumb => {
            thumb.addEventListener('click', () => {
                const newSrc = thumb.getAttribute('data-image');
                mainImage.src = newSrc;
                galleryThumbs.forEach(t => t.classList.remove('active'));
                thumb.classList.add('active');
            });
        });
    } else {
        console.warn('Image gallery elements not found');
    }

    // Add to Cart
    const addToCartForm = document.getElementById('add-to-cart-form');
    const cartToast = document.querySelector('#cartToast') ? new bootstrap.Toast(document.querySelector('#cartToast'), { delay: 3000 }) : null;
    const cartToastBody = document.querySelector('#cartToastBody');
    const addToCartBtn = document.getElementById('addToCart');

    if (addToCartForm && cartToast && cartToastBody && addToCartBtn) {
        addToCartForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const slug = addToCartBtn.getAttribute('data-slug');
            const quantity = parseInt(qtyInput.value);

            if (!slug || isNaN(quantity)) {
                alert('Invalid product or quantity. Please try again.');
                return;
            }

            try {
                addToCartBtn.disabled = true;
                addToCartBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Adding...';

                const response = await fetch('/store/add-to-cart/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                    body: JSON.stringify({ slug, quantity }),
                });

                const data = await response.json();

                if (response.ok && data.status === 'success') {
                    cartToastBody.textContent = data.message;
                    cartToast.show();
                    addToCartBtn.innerHTML = '<i class="fas fa-check"></i> Added';
                    addToCartBtn.classList.add('btn-success');
                    addToCartBtn.classList.remove('btn-primary');
                    const cartBadge = document.getElementById('cartBadge');
                    if (cartBadge) cartBadge.textContent = data.cart_count;
                } else {
                    throw new Error(data.message || 'Failed to add to cart');
                }
            } catch (error) {
                console.error('Add to Cart Error:', error);
                alert(`Error: ${error.message}. Please check your connection or try again later.`);
            } finally {
                setTimeout(() => {
                    addToCartBtn.innerHTML = '<span class="cart-icon">🛒</span> Add to Cart Now';
                    addToCartBtn.classList.add('btn-primary');
                    addToCartBtn.classList.remove('btn-success');
                    addToCartBtn.disabled = false;
                }, 2000);
            }
        });
    } else {
        console.error('Add to cart elements missing');
    }

    // Add to Wishlist
    const addToWishlistForm = document.getElementById('add-to-wishlist-form');
    const wishlistToast = document.querySelector('#wishlistToast') ? new bootstrap.Toast(document.querySelector('#wishlistToast'), { delay: 3000 }) : null;
    const wishlistToastBody = document.getElementById('wishlistToastBody');
    const addToWishlistBtn = document.getElementById('addToWishlist');

    if (addToWishlistForm && wishlistToast && wishlistToastBody && addToWishlistBtn) {
        addToWishlistForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const actionUrl = addToWishlistForm.getAttribute('action');

            try {
                const response = await fetch(actionUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                    body: JSON.stringify({}),
                });

                const data = await response.json();

                if (response.ok && data.status === 'success') {
                    wishlistToastBody.textContent = data.message;
                    wishlistToast.show();
                    if (data.action === 'added') {
                        addToWishlistBtn.classList.add('btn-success');
                        addToWishlistBtn.classList.remove('btn-outline-primary');
                        addToWishlistBtn.innerHTML = '<i class="fas fa-heart"></i> In Wishlist';
                    } else {
                        addToWishlistBtn.classList.add('btn-outline-primary');
                        addToWishlistBtn.classList.remove('btn-success');
                        addToWishlistBtn.innerHTML = '<i class="fas fa-heart"></i> Add to Wishlist';
                    }
                } else {
                    throw new Error(data.message || 'Failed to update wishlist');
                }
            } catch (error) {
                console.error('Wishlist Error:', error);
                alert(`Error: ${error.message}. Please try again.`);
            }
        });
    } else {
        console.error('Wishlist elements missing');
    }
});