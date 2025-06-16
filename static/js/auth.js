// static/js/auth.js
document.addEventListener('DOMContentLoaded', function () {
    // Add password toggle to password fields
    function addPasswordToggle(input) {
        if (!input || input.type !== 'password') return;

        const wrapper = document.createElement('div');
        wrapper.className = 'position-relative';
        input.parentNode.insertBefore(wrapper, input);
        wrapper.appendChild(input);

        const toggle = document.createElement('button');
        toggle.type = 'button';
        toggle.className = 'password-toggle';
        toggle.innerHTML = '<i class="far fa-eye"></i>';
        wrapper.appendChild(toggle);

        toggle.addEventListener('click', function () {
            const isPassword = input.type === 'password';
            input.type = isPassword ? 'text' : 'password';
            const icon = toggle.querySelector('i');
            icon.classList.toggle('fa-eye', isPassword);
            icon.classList.toggle('fa-eye-slash', !isPassword);
        });
    }

    // Apply to all password inputs
    document.querySelectorAll('input[type="password"]').forEach(addPasswordToggle);

    // Handle form submission loading state
    function handleFormSubmit(formId) {
        const form = document.getElementById(formId);
        const submitButton = form.querySelector('.btn-auth');

        if (form && submitButton) {
            form.addEventListener('submit', function (e) {
                submitButton.classList.add('loading');
                submitButton.disabled = true;
            });
        }
    }

    handleFormSubmit('loginForm');
    handleFormSubmit('signupForm');
    handleFormSubmit('logoutForm');
});
