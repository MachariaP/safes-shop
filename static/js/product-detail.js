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

    // Add to Cart Functionality
    const addToCartForm = document.getElementById('add-to-cart-form');
    const cartToast = new bootstrap.Toast(document.getElementById('cartToast'));

    if (addToCartForm && cartToast) {
        addToCartForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(addToCartForm);
            const actionUrl = addToCartForm.getAttribute('action');
            const addToCartBtn = document.getElementById('addToCart');
            const slug = addToCartBtn.dataset.slug;
            const quantity = parseInt(formData.get('quantity'));

            fetch(actionUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Update localStorage
                    let cart = JSON.parse(localStorage.getItem('cart')) || {};
                    cart[slug] = { quantity: (cart[slug]?.quantity || 0) + quantity, price: data.price };
                    localStorage.setItem('cart', JSON.stringify(cart));

                    // Show toast and update button
                    cartToast.show();
                    addToCartBtn.innerHTML = '<i class="fas fa-check"></i> Added';
                    addToCartBtn.classList.add('btn-success');
                    addToCartBtn.classList.remove('btn-primary');
                    setTimeout(() => {
                        addToCartBtn.innerHTML = '<i class="fas fa-shopping-cart"></i> Add to Cart';
                        addToCartBtn.classList.add('btn-primary');
                        addToCartBtn.classList.remove('btn-success');
                    }, 2000);

                    // Update cart badge
                    const cartBadge = document.getElementById('cartBadge');
                    if (cartBadge) {
                        cartBadge.textContent = parseInt(cartBadge.textContent || 0) + quantity;
                    }
                    window.dispatchEvent(new Event('cartUpdated'));
                } else {
                    alert(data.message);
                }
            })
            .catch(error => console.error('Error adding to cart:', error));
        });
    }

    // Add to Wishlist Functionality
    const addToWishlistForm = document.getElementById('add-to-wishlist-form');
    const wishlistToast = new bootstrap.Toast(document.getElementById('wishlistToast'));
    const wishlistToastBody = document.getElementById('wishlistToastBody');

    if (addToWishlistForm && wishlistToast && wishlistToastBody) {
        addToWishlistForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const actionUrl = addToWishlistForm.getAttribute('action');
            const addToWishlistBtn = document.getElementById('addToWishlist');

            fetch(actionUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: JSON.stringify({}),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Update localStorage wishlist
                    let wishlist = JSON.parse(localStorage.getItem('wishlist')) || [];
                    if (data.action === 'added') {
                        if (!wishlist.includes(addToWishlistBtn.dataset.slug)) {
                            wishlist.push(addToWishlistBtn.dataset.slug);
                        }
                    } else {
                        wishlist = wishlist.filter(slug => slug !== addToWishlistBtn.dataset.slug);
                    }
                    localStorage.setItem('wishlist', JSON.stringify(wishlist));

                    // Show toast and update button
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
                    alert(data.message);
                }
            })
            .catch(error => console.error('Error adding to wishlist:', error));
        });
    }
});