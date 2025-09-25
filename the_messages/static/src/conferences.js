document.addEventListener("DOMContentLoaded", () => {

    // Countdown Timer Function
    function updateCountdown() {
        // Set the date we're counting down to
        const dateElement = document.getElementById("upcomingDate")
        const countDownDate = new Date(dateElement.getAttribute("data-date")).getTime();
        const now = new Date().getTime();
        const distance = countDownDate - now;

        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        document.getElementById("days").innerText = days.toString().padStart(2, '0');
        document.getElementById("hours").innerText = hours.toString().padStart(2, '0');
        document.getElementById("minutes").innerText = minutes.toString().padStart(2, '0');
        document.getElementById("seconds").innerText = seconds.toString().padStart(2, '0');

        if (distance < 0) {
            document.getElementById("days").innerText = "00";
            document.getElementById("hours").innerText = "00";
            document.getElementById("minutes").innerText = "00";
            document.getElementById("seconds").innerText = "00";
        }
    }

    // Update the countdown every 1 second
    updateCountdown();
    setInterval(updateCountdown, 1000);

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

    // Observe conference cards for animations
    document.querySelectorAll('.conference-card').forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
        card.style.transitionDelay = `${index * 0.1}s`;
        observer.observe(card);
    });

    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // // Newsletter form handling
    // document.querySelector('button[type="submit"], button:contains("Subscribe")').addEventListener('click', function(e) {
    //     e.preventDefault();
    //     const email = this.previousElementSibling.value;
    //     if (email) {
    //         this.textContent = 'Subscribed!';
    //         this.classList.add('bg-green-500');
    //         setTimeout(() => {
    //             this.textContent = 'Subscribe';
    //             this.classList.remove('bg-green-500');
    //         }, 2000);
    //     }
    // });

    // Add parallax effect to hero section
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const parallax = document.querySelector('.hero-pattern');
        if (parallax) {
            parallax.style.transform = `translateY(${scrolled * 0.1}px)`;
        }
    });

    // Timeline animation on scroll
    const timelineItems = document.querySelectorAll('.relative.flex.items-center');
    timelineItems.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = index % 2 === 0 ? 'translateX(-50px)' : 'translateX(50px)';
        item.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
        item.style.transitionDelay = `${index * 0.2}s`;
        observer.observe(item);
    });
});
