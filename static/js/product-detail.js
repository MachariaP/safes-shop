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
    } else {
        console.warn('Quantity control elements not found');
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
    } else {
        console.warn('Image gallery elements not found');
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
        console.log(`CSRF Token: ${cookieValue}`);
        return cookieValue;
    }

    // Add to Cart Functionality
    const addToCartForm = document.getElementById('add-to-cart-form');
    const cartToast = document.querySelector('#cartToast') ? new bootstrap.Toast(document.querySelector('#cartToast'), { delay: 3000 }) : null;
    const cartToastBody = document.querySelector('#cartToastBody');
    const addToCartBtn = document.getElementById('addToCart');

    if (addToCartForm && cartToast && cartToastBody && addToCartBtn) {
        addToCartForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const slug = addToCartBtn.getAttribute('data-slug');
            const quantity = parseInt(qtyInput.value);
            console.log(`Attempting to add to cart: slug=${slug}, quantity=${quantity}`);

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
                console.log('Response Data:', data);

                if (data.status === 'success') {
                    cartToastBody.textContent = data.message;
                    cartToast.show();
                    addToCartBtn.innerHTML = '<i class="fas fa-check"></i> Added';
                    addToCartBtn.classList.add('btn-success');
                    addToCartBtn.classList.remove('btn-primary');
                    setTimeout(() => {
                        addToCartBtn.innerHTML = '<span class="cart-icon">🛒</span> Add to Cart Now';
                        addToCartBtn.classList.add('btn-primary');
                        addToCartBtn.classList.remove('btn-success');
                        addToCartBtn.disabled = false;
                    }, 2000);
                    const cartBadge = document.getElementById('cartBadge');
                    if (cartBadge) cartBadge.textContent = data.cart_count;
                } else {
                    alert(`Error: ${data.message}`);
                }
            } catch (error) {
                console.error('Fetch Error:', error);
                alert('Failed to add to cart. Check console for details.');
            } finally {
                addToCartBtn.disabled = false;
                addToCartBtn.innerHTML = '<span class="cart-icon">🛒</span> Add to Cart Now';
            }
        });
    } else {
        console.error('Add to cart form, toast, or button missing');
    }

    // Add to Wishlist Functionality
    const addToWishlistForm = document.getElementById('add-to-wishlist-form');
    const wishlistToast = document.querySelector('#wishlistToast') ? new bootstrap.Toast(document.querySelector('#wishlistToast'), { delay: 3000 }) : null;
    const wishlistToastBody = document.getElementById('wishlistToastBody');
    const addToWishlistBtn = document.getElementById('addToWishlist');

    if (addToWishlistForm && wishlistToast && wishlistToastBody && addToWishlistBtn) {
        addToWishlistForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const actionUrl = addToWishlistForm.getAttribute('action');
            console.log(`Attempting wishlist action: url=${actionUrl}`);

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
                console.log('Wishlist Response Data:', data);

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
                    alert(`Error: ${data.message}`);
                }
            } catch (error) {
                console.error('Wishlist Fetch Error:', error);
                alert('Failed to update wishlist. Check console for details.');
            }
        });
    } else {
        console.error('Wishlist form, toast, or button missing');
    }
});
