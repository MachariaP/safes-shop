// static/js/about_us.js
document.addEventListener('DOMContentLoaded', () => {
    // CTA Button Redirect
    const ctaButton = document.getElementById('view-products-cta');
    if (ctaButton) {
        ctaButton.addEventListener('click', (e) => {
            e.preventDefault();
            const targetUrl = ctaButton.getAttribute('href');
            window.location.href = targetUrl;
        });
    }

    // Team Member Modal
    const teamModal = document.getElementById('teamModal');
    if (teamModal) {
        teamModal.addEventListener('show.bs.modal', (event) => {
            const button = event.relatedTarget;
            if (!button) {
                console.error('No trigger button found for modal.');
                return;
            }

            // Get data attributes with fallbacks
            const name = button.getAttribute('data-name') || 'Team Member';
            const title = button.getAttribute('data-title') || 'Position';
            const bio = button.getAttribute('data-bio') || 'No bio available.';
            const imageUrl = button.getAttribute('data-image') || '';

            // Get modal elements
            const modalTitle = teamModal.querySelector('.modal-title');
            const modalSubtitle = teamModal.querySelector('.modal-title-subtitle');
            const modalBio = teamModal.querySelector('.modal-bio');
            const modalImage = teamModal.querySelector('.modal-member-img');

            // Update modal content
            modalTitle.textContent = name;
            modalSubtitle.textContent = title;
            modalBio.textContent = bio;
            
            if (imageUrl && modalImage) {
                modalImage.src = imageUrl;
                modalImage.alt = `${name} - ${title}`;
            } else if (modalImage) {
                modalImage.src = '';
                modalImage.alt = 'No image available';
            }
        });
    } else {
        console.error('Team modal element not found.');
    }

    // Enhanced hover effect for team member cards
    const teamMembers = document.querySelectorAll('.team-member');
    if (teamMembers.length > 0) {
        teamMembers.forEach(member => {
            member.addEventListener('mouseenter', () => {
                member.style.transform = 'translateY(-5px)';
                member.style.boxShadow = '0 10px 20px rgba(0, 0, 0, 0.1)';
                member.style.backgroundColor = '#f8fbff';
                member.style.borderColor = '#cfe2ff';
            });
            
            member.addEventListener('mouseleave', () => {
                member.style.transform = '';
                member.style.boxShadow = '';
                member.style.backgroundColor = '';
                member.style.borderColor = '#e9ecef';
            });
        });
    } else {
        console.warn('No team members found.');
    }
});