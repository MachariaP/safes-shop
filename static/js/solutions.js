// static/js/solutions.js
document.addEventListener('DOMContentLoaded', () => {
    // Smooth scrolling for solution navigation
    const navButtons = document.querySelectorAll('.solution-nav-btn');
    
    navButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = button.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                navButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Animate solution cards on scroll
    const solutionCards = document.querySelectorAll('.solution-card');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate__animated', 'animate__fadeInUp');
                observer.unobserve(entry.target);
            }
        });
    }, { rootMargin: '0px', threshold: 0.2 });

    solutionCards.forEach(card => observer.observe(card));
});