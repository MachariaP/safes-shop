// static/js/product_list.js
document.addEventListener('DOMContentLoaded', () => {
    // Card Hover Effect
    // Adds a lift and shadow effect on mouse hover
    const cards = document.querySelectorAll('.card');

    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-5px)';
            card.style.boxShadow = '0 12px 40px rgba(0, 0, 0, 0.12)';
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
            card.style.boxShadow = '0 8px 30px rgba(0, 0, 0, 0.08)';
        });
    });

    // Add to Cart Functionality
    // Handles adding a product to the cart via AJAX
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    const cartToast = document.querySelector('#cartToast') ? new bootstrap.Toast(document.querySelector('#cartToast'), { delay: 3000 }) : null;
    const cartToastBody = document.querySelector('#cartToastBody');

    if (!addToCartButtons.length) console.warn('No add-to-cart buttons found');
    if (!cartToast || !cartToastBody) console.warn('Cart toast or body element missing');

    addToCartButtons.forEach(button => {
        button.addEventListener('click', async (e) => {
            e.preventDefault();
            const slug = button.getAttribute('data-slug');
            const quantity = 1; // Default quantity for list view
            console.log(`Attempting to add to cart: slug=${slug}, quantity=${quantity}`); // Debug log

            try {
                const response = await fetch('/store/add-to-cart/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                    body: JSON.stringify({ slug, quantity }),
                });
                console.log(`Response Status: ${response.status}`); // Debug log
                const data = await response.json();
                console.log('Response Data:', data); // Debug log

                if (data.status === 'success') {
                    if (cartToast && cartToastBody) {
                        cartToastBody.textContent = data.message;
                        cartToast.show();
                        button.innerHTML = '<i class="fas fa-check"></i> Added';
                        button.classList.add('btn-success');
                        button.classList.remove('btn-primary');
                        button.disabled = true;
                        setTimeout(() => {
                            button.innerHTML = '<i class="fas fa-shopping-cart"></i> Add to Cart';
                            button.classList.add('btn-primary');
                            button.classList.remove('btn-success');
                            button.disabled = false;
                        }, 2000);
                    } else {
                        alert(data.message); // Fallback
                    }
                    window.dispatchEvent(new Event('cartUpdated'));
                    const cartBadge = document.getElementById('cartBadge');
                    if (cartBadge) cartBadge.textContent = data.cart_count;
                } else {
                    console.error('Server Error:', data.message);
                    alert(`Error: ${data.message}`);
                }
            } catch (error) {
                console.error('Fetch Error:', error);
                alert('Failed to add to cart. Check console for details.');
            }
        });
    });

    // Helper function to get CSRF token
    // Retrieves the CSRF token from cookies for AJAX requests
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
        console.log(`CSRF Token: ${cookieValue}`); // Debug log
        return cookieValue;
    }

    // Note: "Load More" functionality removed to rely on Django pagination
});
