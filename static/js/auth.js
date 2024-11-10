document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.tab');
    const forms = document.querySelectorAll('.form');

    // Tab switching logic
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            forms.forEach(f => f.classList.remove('active'));
            tab.classList.add('active');
            document.querySelector(`.form#${tab.dataset.tab}Form`).classList.add('active');
        });
    });
});
