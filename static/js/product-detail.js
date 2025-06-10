// static/js/product-detail.js

document.addEventListener('DOMContentLoaded', () => {
    // Quantity control
    const decreaseQty = document.getElementById('decreaseQty');
    const increaseQty = document.getElementById('increaseQty');
    const qtyInput = document.getElementById('productQty');

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

    // Image gallery functionality
    const galleryThumbs = document.querySelectorAll('.gallery-thumb');
    const mainImage = document.getElementById('mainProductImage');

    galleryThumbs.forEach(thumb => {
        thumb.addEventListener('click', () => {
            const newSrc = thumb.getAttribute('data-image');
            mainImage.src = newSrc;
            galleryThumbs.forEach(t => t.classList.remove('active'));
            thumb.classList.add('active');
        });
    });

    // Add to cart functionality
    const addToCartBtn = document.getElementById('addToCart');
    const toast = new bootstrap.Toast(document.getElementById('cartToast'));

    addToCartBtn.addEventListener('click', () => {
        const quantity = qtyInput.value;
        const productName = document.querySelector('.product-title').textContent;
        document.querySelector('.toast-body').textContent = `${productName} (${quantity} item${quantity > 1 ? 's' : ''}) has been added to your cart.`;
        toast.show();

        addToCartBtn.innerHTML = '<i class="fas fa-check"></i> Added';
        addToCartBtn.classList.add('btn-success');
        addToCartBtn.classList.remove('btn-primary');

        setTimeout(() => {
            addToCartBtn.innerHTML = '<i class="fas fa-shopping-cart"></i> Add to Cart';
            addToCartBtn.classList.add('btn-primary');
            addToCartBtn.classList.remove('btn-success');
        }, 2000);
    });
});