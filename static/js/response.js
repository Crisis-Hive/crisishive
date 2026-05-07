// Highlight selected team card on click
document.querySelectorAll('.team-option').forEach(option => {
    option.addEventListener('click', () => {
        document.querySelectorAll('.team-option__card').forEach(card => {
            card.style.borderColor = '';
        });
    });
});