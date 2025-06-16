// static/js/contact.js
document.addEventListener('DOMContentLoaded', () => {
    // Initialize Google Map
    function initMap() {
        const nairobi = { lat: -1.2921, lng: 36.8219 };
        
        const map = new google.maps.Map(document.getElementById('map'), {
            zoom: 15,
            center: nairobi,
            styles: [
                {
                    "featureType": "administrative",
                    "elementType": "labels.text.fill",
                    "stylers": [{"color": "#444444"}]
                },
                {
                    "featureType": "landscape",
                    "elementType": "all",
                    "stylers": [{"color": "#f2f2f2"}]
                },
                {
                    "featureType": "poi",
                    "elementType": "all",
                    "stylers": [{"visibility": "off"}]
                },
                {
                    "featureType": "road",
                    "elementType": "all",
                    "stylers": [{"saturation": -100}, {"lightness": 45}]
                },
                {
                    "featureType": "road.highway",
                    "elementType": "all",
                    "stylers": [{"visibility": "simplified"}]
                },
                {
                    "featureType": "road.arterial",
                    "elementType": "labels.icon",
                    "stylers": [{"visibility": "off"}]
                },
                {
                    "featureType": "transit",
                    "elementType": "all",
                    "stylers": [{"visibility": "off"}]
                },
                {
                    "featureType": "water",
                    "elementType": "all",
                    "stylers": [{"color": "#d4e4f3"}, {"visibility": "on"}]
                }
            ]
        });
        
        new google.maps.Marker({
            position: nairobi,
            map: map,
            title: 'Diplomat Safes Nairobi',
            icon: {
                url: "https://maps.google.com/mapfiles/ms/icons/blue-dot.png"
            }
        });
        
        const contentString = `
            <div class="map-info-window">
                <h3>Diplomat Safes</h3>
                <p>123 Security Street, Industrial Area</p>
                <p>Nairobi, Kenya</p>
                <p><i class="fas fa-phone me-1"></i> +254 712 345 678</p>
            </div>
        `;
        
        const infowindow = new google.maps.InfoWindow({
            content: contentString
        });
        
        infowindow.open(map);
    }
    
    window.initMap = initMap;
    
    // Form submission handling
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const name = document.getElementById('name').value.trim();
            const email = document.getElementById('email').value.trim();
            const subject = document.getElementById('subject').value.trim();
            const message = document.getElementById('message').value.trim();
            const phone = document.getElementById('phone').value.trim();
            
            if (!name || !email || !subject || !message) {
                alert('Please fill in all required fields.');
                return;
            }
            
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                alert('Please enter a valid email address.');
                return;
            }
            
            const originalButtonText = contactForm.querySelector('button[type="submit"]').innerHTML;
            contactForm.querySelector('button[type="submit"]').innerHTML = 
                '<i class="fas fa-check me-2"></i> Message Sent!';
            
            setTimeout(() => {
                contactForm.querySelector('button[type="submit"]').innerHTML = originalButtonText;
                contactForm.reset();
            }, 3000);
        });
    }
    
    const accordions = document.querySelectorAll('.accordion-button');
    accordions.forEach(accordion => {
        accordion.addEventListener('click', function() {
            const icon = this.querySelector('i');
            if (icon) {
                icon.classList.toggle('fa-chevron-down');
                icon.classList.toggle('fa-chevron-up');
            }
        });
    });
});