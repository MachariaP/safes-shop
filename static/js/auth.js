document.addEventListener('DOMContentLoaded', function () {
    // Add touch support for auth card
    const authCard = document.querySelector('.auth-card');
    if (authCard) {
        authCard.addEventListener('touchstart', () => {
            authCard.classList.add('touched');
        });
        authCard.addEventListener('touchend', () => {
            setTimeout(() => authCard.classList.remove('touched'), 1000);
        });
    }

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

    // Handle login button visibility based on form inputs
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        const usernameInput = loginForm.querySelector('input[name="login"]');
        const passwordInput = loginForm.querySelector('input[name="password"]');
        const loginButton = loginForm.querySelector('.btn-auth');

        function toggleLoginButton() {
            if (usernameInput && passwordInput && loginButton) {
                const isValid = usernameInput.value.trim() !== '' && passwordInput.value.trim() !== '';
                loginButton.classList.toggle('btn-hidden', !isValid);
            }
        }

        if (usernameInput && passwordInput) {
            // Initial check
            toggleLoginButton();
            // Add input listeners with debounce
            let debounceTimeout;
            const debounceToggle = () => {
                clearTimeout(debounceTimeout);
                debounceTimeout = setTimeout(toggleLoginButton, 100);
            };
            usernameInput.addEventListener('input', debounceToggle);
            passwordInput.addEventListener('input', debounceToggle);
            // Prevent hiding on focus
            loginButton.addEventListener('focus', () => {
                if (usernameInput.value.trim() !== '' && passwordInput.value.trim() !== '') {
                    loginButton.classList.remove('btn-hidden');
                }
            });
        }
    }

    // Handle form submission loading state
    function handleFormSubmit(formId) {
        const form = document.getElementById(formId);
        const submitButton = form ? form.querySelector('.btn-auth') : null;

        if (form && submitButton) {
            form.addEventListener('submit', function (e) {
                if (formId === 'loginForm') {
                    // Login form: validate inputs
                    const usernameInput = form.querySelector('input[name="login"]');
                    const passwordInput = form.querySelector('input[name="password"]');
                    if (!usernameInput || !passwordInput || usernameInput.value.trim() === '' || passwordInput.value.trim() === '') {
                        e.preventDefault();
                        return;
                    }
                }
                // Apply loading state for all forms
                submitButton.classList.add('loading');
                submitButton.disabled = true;
            });
        } else {
            console.warn(`Form with ID ${formId} or submit button not found`);
        }
    }

    handleFormSubmit('loginForm');
    handleFormSubmit('logoutForm');
    handleFormSubmit('signupForm');
});