// Tab switching
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
    });
});

// Avatar preview on file select
const avatarInput = document.getElementById('avatarInput');
if (avatarInput) {
    avatarInput.addEventListener('change', () => {
        const file = avatarInput.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = e => {
            const existing = document.querySelector('.profile-header__avatar img');
            const placeholder = document.querySelector('.avatar-placeholder');
            if (existing) {
                existing.src = e.target.result;
            } else if (placeholder) {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.alt = 'Avatar';
                placeholder.replaceWith(img);
            }
        };
        reader.readAsDataURL(file);
    });
}