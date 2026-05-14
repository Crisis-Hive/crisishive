// Tab switching
document.querySelectorAll('.profile-tab').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.profile-tab').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.profile-tab-content').forEach(c => c.classList.remove('active'));
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
            const existing = document.querySelector('.profile-avatar img');
            const placeholder = document.querySelector('.profile-avatar--placeholder');
            if (existing) {
                existing.src = e.target.result;
            } else if (placeholder) {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.alt = 'Avatar';
                img.className = 'profile-avatar';
                placeholder.replaceWith(img);
            }
        };
        reader.readAsDataURL(file);
    });
}