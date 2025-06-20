document.addEventListener('DOMContentLoaded', () => {
    // Smooth scrolling for solution navigation
    const navButtons = document.querySelectorAll('.solution-nav-btn');
    navButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = button.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                navButtons.forEach(btn => btn.setAttribute('aria-selected', 'false'));
                button.setAttribute('aria-selected', 'true');
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Animate solution cards on scroll
    const solutionCards = document.querySelectorAll('.solution-card');
    const cardObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate__animated', 'animate__fadeInUp');
                cardObserver.unobserve(entry.target);
            }
        });
    }, { rootMargin: '0px', threshold: 0.2 });
    solutionCards.forEach(card => cardObserver.observe(card));

    // Dynamic content reveal for solution features
    const featureToggles = document.querySelectorAll('.feature-toggle');
    featureToggles.forEach(toggle => {
        toggle.addEventListener('click', () => {
            const list = toggle.nextElementSibling;
            const isOpen = list.getAttribute('aria-hidden') === 'false';
            list.setAttribute('aria-hidden', isOpen ? 'true' : 'false');
            list.style.maxHeight = isOpen ? '0' : `${list.scrollHeight}px`;
        });
        toggle.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                toggle.click();
            }
        });
    });

    // Lazy loading for images
    const lazyImages = document.querySelectorAll('img[loading="lazy"]');
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                imageObserver.unobserve(img);
            }
        });
    }, { rootMargin: '0px 0px 100px 0px' });
    lazyImages.forEach(img => imageObserver.observe(img));

    // Lightbox functionality
    const lightbox = document.querySelector('.lightbox');
    const lightboxImage = lightbox.querySelector('.lightbox-image');
    const lightboxTriggers = document.querySelectorAll('.lightbox-trigger');
    lightboxTriggers.forEach(trigger => {
        trigger.addEventListener('click', () => {
            lightboxImage.src = trigger.src;
            lightboxImage.alt = trigger.alt;
            lightbox.style.display = 'flex';
            lightbox.focus();
        });
    });
    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) {
            lightbox.style.display = 'none';
        }
    });
    lightbox.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            lightbox.style.display = 'none';
        }
    });
});