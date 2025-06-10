// static/js/product_list.js

document.addEventListener('DOMContentLoaded', () => {
    // Card Hover Effect
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

    // Placeholder for Load More Functionality
    let visibleCards = 6; // Initial number of cards to show
    const allCards = document.querySelectorAll('.col-lg-4');
    const loadMoreBtn = document.createElement('button');

    if (allCards.length > visibleCards) {
        loadMoreBtn.textContent = 'Load More';
        loadMoreBtn.className = 'btn btn-outline-primary w-100 mt-4';
        document.querySelector('.row').after(loadMoreBtn);

        loadMoreBtn.addEventListener('click', () => {
            visibleCards += 6; // Load 6 more cards
            allCards.forEach((card, index) => {
                if (index < visibleCards) card.style.display = 'block';
            });
            if (visibleCards >= allCards.length) loadMoreBtn.style.display = 'none';
        });

        // Hide excess cards initially
        allCards.forEach((card, index) => {
            if (index >= visibleCards) card.style.display = 'none';
        });
    }

    // Smooth Scroll on Detail Click
	/*
    const detailLinks = document.querySelectorAll('.btn-outline-primary');
    detailLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const href = link.getAttribute('href');
            document.querySelector(href).scrollIntoView({ behavior: 'smooth' });
        });
    });
    */
});
