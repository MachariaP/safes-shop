// static/js/about_us.js
document.addEventListener('DOMContentLoaded', () => {
    const ctaButton = document.getElementById('view-products-cta');
    if (ctaButton) {
        ctaButton.addEventListener('click', (e) => {
            const target = document.querySelector(e.target.getAttribute('href'));
            if (target) {
                e.preventDefault();
                window.scrollTo({
                    top: target.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    }
});
