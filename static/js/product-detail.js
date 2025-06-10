// static/js/product-detail.js

document.addEventListener('DOMContentLoaded', () => {
    // Quantity Control
    const decreaseQty = document.getElementById('decreaseQty');
    const increaseQty = document.getElementById('increaseQty');
    const qtyInput = document.getElementById('productQty');

    if (decreaseQty && increaseQty && qtyInput) {
        decreaseQty.addEventListener('click', () => {
            let value = parseInt(qtyInput.value);
            if (value > 1) qtyInput.value = value - 1;
        });

        increaseQty.addEventListener('click', () => {
            let value = parseInt(qtyInput.value);
            if (value < 10) qtyInput.value = value + 1;
        });

        qtyInput.addEventListener('input', () => {
            let value = parseInt(qtyInput.value);
            if (isNaN(value) || value < 1) qtyInput.value = 1;
            else if (value > 10) qtyInput.value = 10;
        });
    }

    // Image Gallery Functionality
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
    }

    // Add to Cart Functionality
    const addToCartBtn = document.getElementById('addToCart');
    const cartToast = new bootstrap.Toast(document.getElementById('cartToast'));
    const toastBody = document.querySelector('#cartToast .toast-body');

    if (addToCartBtn && cartToast && toastBody) {
        addToCartBtn.addEventListener('click', () => {
            const slug = addToCartBtn.getAttribute('data-slug');
            const quantity = qtyInput ? parseInt(qtyInput.value) : 1;
            fetch(`/store/add-to-cart/${slug}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: `quantity=${quantity}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    toastBody.textContent = data.message;
                    cartToast.show();
                    addToCartBtn.innerHTML = '<i class="fas fa-check"></i> Added';
                    addToCartBtn.classList.add('btn-success');
                    addToCartBtn.classList.remove('btn-primary');
                    setTimeout(() => {
                        addToCartBtn.innerHTML = '<i class="fas fa-shopping-cart"></i> Add to Cart';
                        addToCartBtn.classList.add('btn-primary');
                        addToCartBtn.classList.remove('btn-success');
                    }, 2000);

                    // Dispatch custom event to update cart badge
                    window.dispatchEvent(new Event('cartUpdated'));
                } else {
                    console.error(data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    // Add to Wishlist Functionality
    const addToWishlistBtn = document.getElementById('addToWishlist');
    const wishlistToast = new bootstrap.Toast(document.getElementById('wishlistToast'));
    const wishlistToastBody = document.getElementById('wishlistToastBody');

    if (addToWishlistBtn && wishlistToast && wishlistToastBody) {
        addToWishlistBtn.addEventListener('click', () => {
            const slug = addToWishlistBtn.getAttribute('data-slug');
            fetch(`/store/add-to-wishlist/${slug}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken'),
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
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
                    console.error(data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    // Helper function to get CSRF token
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
});