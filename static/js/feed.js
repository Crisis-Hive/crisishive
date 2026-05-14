// ── Upvote (feed + detail) ──
document.querySelectorAll('.upvote-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
        const id = btn.dataset.id;
        if (!id) return;
        try {
            const res = await fetch(`/crisis/${id}/upvote/`, {
                method: 'POST',
                headers: { 'X-CSRFToken': getCookie('csrftoken') }
            });
            const data = await res.json();
            const countEl = btn.querySelector('.upvote-count') || document.getElementById('upvoteCount');
            if (countEl) countEl.textContent = data.count;
            btn.classList.toggle('upvote-btn--active', data.upvoted);
        } catch (e) {
            console.error('Upvote failed', e);
        }
    });
});

// ── Report Crisis — Leaflet Map ──
const reportMap = document.getElementById('reportMap');
if (reportMap) {
    const map = L.map('reportMap').setView([23.8103, 90.4125], 7); // Bangladesh center
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

    let marker = null;
    const latInput = document.getElementById('latInput');
    const lngInput = document.getElementById('lngInput');
    const locationDisplay = document.getElementById('locationDisplay');

    map.on('click', (e) => {
        const { lat, lng } = e.latlng;
        if (marker) marker.setLatLng([lat, lng]);
        else marker = L.marker([lat, lng]).addTo(map);
        latInput.value = lat.toFixed(6);
        lngInput.value = lng.toFixed(6);
        locationDisplay.textContent = `Selected: ${lat.toFixed(5)}, ${lng.toFixed(5)}`;
        locationDisplay.style.color = '#00c853';
    });
}

// ── Dropzone ──
const dropzone = document.getElementById('dropzone');
const mediaInput = document.getElementById('mediaInput');
const mediaPreview = document.getElementById('mediaPreview');
const dropzoneInner = document.getElementById('dropzoneInner');

if (dropzone && mediaInput) {
    dropzone.addEventListener('click', () => mediaInput.click());

    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('dragover');
    });

    dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));

    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('dragover');
        handleFiles(e.dataTransfer.files);
    });

    mediaInput.addEventListener('change', () => handleFiles(mediaInput.files));

    function handleFiles(files) {
        mediaPreview.innerHTML = '';
        if (files.length > 0) dropzoneInner.style.display = 'none';
        Array.from(files).forEach(file => {
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = e => {
                    const img = document.createElement('img');
                    img.src = e.target.result;
                    mediaPreview.appendChild(img);
                };
                reader.readAsDataURL(file);
            }
        });
    }
}

// ── Report form loading state ──
const reportForm = document.getElementById('reportForm');
if (reportForm) {
    reportForm.addEventListener('submit', () => {
        const btn = document.getElementById('submitBtn');
        if (btn) {
            btn.disabled = true;
            btn.querySelector('.btn-text').hidden = true;
            btn.querySelector('.btn-loader').hidden = false;
        }
    });
}

// ── CSRF helper ──
function getCookie(name) {
    const val = `; ${document.cookie}`;
    const parts = val.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}