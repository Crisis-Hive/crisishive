// ── Auto-dismiss messages with animation ──
document.querySelectorAll('.message').forEach(msg => {
    setTimeout(() => {
        msg.classList.add('message--dismissing');
        setTimeout(() => msg.remove(), 400);
    }, 4000);
});

// ── Mobile Menu ──
const burger = document.getElementById('navBurger');
const overlay = document.getElementById('navOverlay');
const mobileMenu = document.getElementById('navMobile');
const closeBtn = document.getElementById('navClose');

function openMobileMenu() {
    overlay.classList.add('open');
    mobileMenu.classList.add('open');
    document.body.style.overflow = 'hidden';
}

function closeMobileMenu() {
    overlay.classList.remove('open');
    mobileMenu.classList.remove('open');
    document.body.style.overflow = '';
}

if (burger) burger.addEventListener('click', openMobileMenu);
if (overlay) overlay.addEventListener('click', closeMobileMenu);
if (closeBtn) closeBtn.addEventListener('click', closeMobileMenu);

// Close on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && mobileMenu?.classList.contains('open')) {
        closeMobileMenu();
    }
});

// ── Navbar scroll effect ──
const navbar = document.getElementById('mainNav');
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const currentScroll = window.scrollY;
    if (navbar) {
        if (currentScroll > 50) {
            navbar.style.background = 'rgba(10, 10, 10, 0.92)';
        } else {
            navbar.style.background = 'rgba(10, 10, 10, 0.75)';
        }
    }
    lastScroll = currentScroll;
}, { passive: true });