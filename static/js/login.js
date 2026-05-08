// Toggle password visibility
const togglePw = document.getElementById('togglePw');
const passwordInput = document.getElementById('password');

if (togglePw && passwordInput) {
    togglePw.addEventListener('click', () => {
        const isHidden = passwordInput.type === 'password';
        passwordInput.type = isHidden ? 'text' : 'password';
        togglePw.textContent = isHidden ? 'Hide' : 'Show';
    });
}

// Client-side validation + loading state
const loginForm = document.getElementById('loginForm');
const submitBtn = document.getElementById('submitBtn');
const btnText = submitBtn?.querySelector('.btn-text');
const btnLoader = submitBtn?.querySelector('.btn-loader');
const emailError = document.getElementById('emailError');
const passwordError = document.getElementById('passwordError');

if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
        let valid = true;

        // Clear previous errors
        emailError.textContent = '';
        passwordError.textContent = '';

        const email = document.getElementById('email').value.trim();
        const password = passwordInput.value;

        if (!email) {
            emailError.textContent = 'Email is required.';
            valid = false;
        }

        if (!password) {
            passwordError.textContent = 'Password is required.';
            valid = false;
        }

        if (!valid) {
            e.preventDefault();
            return;
        }

        // Loading state
        submitBtn.disabled = true;
        btnText.hidden = true;
        btnLoader.hidden = false;
    });
}