document.addEventListener("DOMContentLoaded", () => {
    // Filter functionality
    const messageCards = document.querySelectorAll('.message-card');


    // View toggle functionality
    const gridView = document.getElementById('gridView');
    const listView = document.getElementById('listView');
    const messagesGrid = document.getElementById('messagesGrid');

    gridView.addEventListener('click', () => {
        gridView.classList.remove('bg-gray-700');
        gridView.classList.add('bg-purple-600');
        listView.classList.remove('bg-purple-600');
        listView.classList.add('bg-gray-700');
        messagesGrid.className = 'grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8';
    });

    listView.addEventListener('click', () => {
        listView.classList.remove('bg-gray-700');
        listView.classList.add('bg-purple-600');
        gridView.classList.remove('bg-purple-600');
        gridView.classList.add('bg-gray-700');
        messagesGrid.className = 'flex flex-col gap-6';
    });

    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe all message cards
    messageCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        card.style.transitionDelay = `${index * 0.1}s`;
        observer.observe(card);
    });

    const sortSelect = document.getElementById('sortSelect');
    if (sortSelect) {
        sortSelect.addEventListener('change', function () {
            const params = new URLSearchParams(window.location.search);
            params.set('sort', sortSelect.value);
            window.location.search = params.toString();
        });
    }
});
