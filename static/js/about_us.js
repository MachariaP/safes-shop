// static/js/about_us.js
document.addEventListener('DOMContentLoaded', () => {
    // CTA Button Smooth Scroll
    const ctaButton = document.getElementById('view-products-cta');
    if (ctaButton) {
        ctaButton.addEventListener('click', (e) => {
            e.preventDefault();
            const targetUrl = ctaButton.getAttribute('href');
            window.location.href = targetUrl; // Redirect to store page for now
            // Uncomment below if you want scroll behavior instead
            // const target = document.querySelector(targetUrl);
            // if (target) {
            //     window.scrollTo({
            //         top: target.offsetTop - 80,
            //         behavior: 'smooth'
            //     });
            // }
        });
    }

    // Team Member Modal
    const teamModal = document.getElementById('teamModal');
    if (teamModal) {
        teamModal.addEventListener('show.bs.modal', (event) => {
            const button = event.relatedTarget;
            const name = button.getAttribute('data-name');
            const title = button.getAttribute('data-title');
            const bio = button.getAttribute('data-bio');

            const modalTitle = teamModal.querySelector('.modal-title');
            const modalSubtitle = teamModal.querySelector('.modal-title-subtitle');
            const modalBio = teamModal.querySelector('.modal-bio');

            modalTitle.textContent = name;
            modalSubtitle.textContent = title;
            modalBio.textContent = bio || 'No bio available.';
        });
    }

    // Optional: Add hover effect for team images
    const teamImages = document.querySelectorAll('.team-img');
    teamImages.forEach(img => {
        img.addEventListener('mouseover', () => {
            img.style.borderColor = '#0056b3';
        });
        img.addEventListener('mouseout', () => {
            img.style.borderColor = '#0d6efd';
        });
    });
});