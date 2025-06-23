document.addEventListener('DOMContentLoaded', () => {
    // Card Hover and Touch Effects
    const cards = document.querySelectorAll('.product-card');
    cards.forEach(card => {
        // Mouse hover effects
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-8px)';
            card.style.boxShadow = '0 15px 40px rgba(0, 0, 0, 0.12)';
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
            card.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.08)';
        });

        // Touch effects for mobile devices
        card.addEventListener('touchstart', () => {
            card.classList.add('hover');
        });
        card.addEventListener('touchend', () => {
            // Remove hover class after a short delay to mimic hover-out
            setTimeout(() => card.classList.remove('hover'), 1000);
        });
    });

    // Add to Cart Functionality
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    const cartToast = document.querySelector('#cartToast') ? new bootstrap.Toast(document.querySelector('#cartToast')) : null;
    const cartToastBody = document.querySelector('#cartToastBody');

    if (!addToCartButtons.length) console.warn('No add-to-cart buttons found');
    if (!cartToast || !cartToastBody) console.warn('Cart toast or body element missing');

    addToCartButtons.forEach(button => {
        button.addEventListener('click', async (e) => {
            e.preventDefault();
            const slug = button.getAttribute('data-slug');
            const quantity = 1;
            console.log(`Attempting to add to cart: slug=${slug}, quantity=${quantity}`);

            try {
                button.disabled = true;
                button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Adding...';
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
                    if (cartToast && cartToastBody) {
                        cartToastBody.textContent = data.message;
                        cartToast.show();
                    } else {
                        alert(data.message);
                    }
                    const cartBadge = document.getElementById('cartBadge');
                    if (cartBadge) cartBadge.textContent = data.cart_count;
                    button.innerHTML = '<i class="fas fa-check"></i> Added';
                    button.classList.add('btn-success');
                    button.classList.remove('btn-primary');
                    setTimeout(() => {
                        button.innerHTML = '<span class="cart-icon">🛒</span> Add to Cart Now';
                        button.classList.add('btn-primary');
                        button.classList.remove('btn-success');
                        button.disabled = false;
                    }, 2000);
                } else {
                    alert(`Error: ${data.message}`);
                }
            } catch (error) {
                console.error('Fetch Error:', error);
                alert('Failed to add to cart. Check console for details.');
            } finally {
                button.disabled = false;
                button.innerHTML = '<span class="cart-icon">🛒</span> Add to Cart Now';
            }
        });
    });

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
});