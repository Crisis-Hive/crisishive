// Donate page — toggle money/resource fields
const toggleBtns = document.querySelectorAll('.donate-toggle-btn');
const moneyField = document.getElementById('moneyField');
const resourceField = document.getElementById('resourceField');

if (toggleBtns.length) {
    toggleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            toggleBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const type = btn.dataset.type;
            if (type === 'money') {
                moneyField.style.display = '';
                resourceField.style.display = 'none';
            } else if (type === 'resource') {
                moneyField.style.display = 'none';
                resourceField.style.display = '';
            } else {
                moneyField.style.display = '';
                resourceField.style.display = '';
            }
        });
    });
}