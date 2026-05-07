const togglePw = document.getElementById('togglePw');
const passwordInput = document.getElementById('password');

if (togglePw && passwordInput) {
    togglePw.addEventListener('click', () => {
        const isHidden = passwordInput.type === 'password';
        passwordInput.type = isHidden ? 'text' : 'password';
        togglePw.textContent = isHidden ? 'Hide' : 'Show';
    });
}

const registerForm = document.getElementById('registerForm');
const submitBtn = document.getElementById('submitBtn');
const btnText = submitBtn?.querySelector('.btn-text');
const btnLoader = submitBtn?.querySelector('.btn-loader');

if (registerForm) {
    registerForm.addEventListener('submit', (e) => {
        let valid = true;

        document.querySelectorAll('.form-group__error').forEach(el => el.textContent = '');

        const email = document.getElementById('email').value.trim();
        const username = document.getElementById('username').value.trim();
        const password = passwordInput.value;
        const role = document.getElementById('role').value;

        if (!email) { document.getElementById('emailError').textContent = 'Email is required.'; valid = false; }
        if (!username) { document.getElementById('usernameError').textContent = 'Username is required.'; valid = false; }
        if (password.length < 8) { document.getElementById('passwordError').textContent = 'Password must be at least 8 characters.'; valid = false; }
        if (!role) { document.getElementById('roleError').textContent = 'Please select a role.'; valid = false; }

        if (!valid) { e.preventDefault(); return; }

        submitBtn.disabled = true;
        btnText.hidden = true;
        btnLoader.hidden = false;
    });
}