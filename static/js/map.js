// ── CrisisHive Crisis Map ──

const severityColors = {
    critical: '#E8001D',
    high:     '#ff6d00',
    medium:   '#ffd600',
    low:      '#00c853',
};

// Init map centered on Bangladesh
const map = L.map('crisisMap').setView([23.8103, 90.4125], 7);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Build markers
const allMarkers = [];

function makeIcon(color) {
    return L.divIcon({
        className: '',
        html: `<div style="
            width:14px; height:14px;
            background:${color};
            border:2px solid #fff;
            border-radius:50%;
            box-shadow:0 0 6px ${color}88;
        "></div>`,
        iconSize: [14, 14],
        iconAnchor: [7, 7],
    });
}

window.CRISIS_DATA.forEach(crisis => {
    const color = severityColors[crisis.severity] || '#888';
    const marker = L.marker([crisis.lat, crisis.lng], { icon: makeIcon(color) });

    marker.bindPopup(`
        <div class="popup-content">
            <p class="popup-content__title">${crisis.title}</p>
            <p class="popup-content__meta">${crisis.category} · ${crisis.severity} · ${crisis.status}</p>
            <a href="/crisis/${crisis.id}/">View Details</a>
        </div>
    `);

    marker.crisisData = crisis;
    marker.addTo(map);
    allMarkers.push(marker);
});

// ── Filters ──
function applyFilters() {
    const districtVal = document.getElementById('districtFilter').value.toLowerCase();
    const checkedSeverities = Array.from(
        document.querySelectorAll('.severity-checks input:checked')
    ).map(cb => cb.value);

    allMarkers.forEach(marker => {
        const c = marker.crisisData;
        const districtMatch = !districtVal || (c.district && c.district.toLowerCase() === districtVal);
        const severityMatch = checkedSeverities.includes(c.severity);

        if (districtMatch && severityMatch) {
            marker.addTo(map);
        } else {
            map.removeLayer(marker);
        }
    });
}

document.getElementById('districtFilter').addEventListener('change', applyFilters);
document.querySelectorAll('.severity-checks input').forEach(cb => {
    cb.addEventListener('change', applyFilters);
});
