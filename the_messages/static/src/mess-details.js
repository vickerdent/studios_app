document.addEventListener("DOMContentLoaded", () => {

    // Audio player functionality
    let isPlaying = false;
    let currentTime = 0;

    const playButton = document.getElementById('playButton');
    const audioProgress = document.getElementById('audioProgress');
    const audio = document.querySelector('audio');

    const totalDuration = Number(playButton.getAttribute("data-time"));

    playButton.addEventListener('click', () => {
        isPlaying = !isPlaying;

        if (isPlaying) {
            playButton.innerHTML = `
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd"></path>
                </svg>
            `;
            startAudioProgress();
            audio.play();
        } else {
            playButton.innerHTML = `
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd"></path>
                </svg>
            `;
            audio.pause();
        }
    });

    function startAudioProgress() {
        if (!isPlaying) return;

        currentTime += 1;
        if (currentTime > totalDuration) {
            currentTime = totalDuration;
            isPlaying = false;
            playButton.innerHTML = `
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd"></path>
                </svg>
            `;
        }

        const progressPercent = (currentTime / totalDuration) * 100;
        audioProgress.style.width = progressPercent + '%';

        const minutes = Math.floor(currentTime / 60);
        const seconds = currentTime % 60;
        const timeDisplay = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        document.querySelector('.text-sm.text-gray-400.w-16').textContent = timeDisplay;

        if (isPlaying) {
            setTimeout(startAudioProgress, 1000);
        }
    }

    // Smooth animations on scroll
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

    // Observe slide-up elements
    document.querySelectorAll('.slide-up').forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        element.style.transitionDelay = `${index * 0.1}s`;
        observer.observe(element);
    });
});

// Download functionality
function downloadAudio(fileUrl, name) {
    const progressDiv = document.getElementById('downloadProgress');
    const progressFill = document.getElementById('progressFill');
    const progressPercent = document.getElementById('progressPercent');

    progressDiv.classList.remove('hidden');

    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress > 100) progress = 100;

        progressFill.style.width = progress + '%';
        progressPercent.textContent = Math.round(progress) + '%';

        if (progress >= 100) {
            clearInterval(interval);
            setTimeout(() => {
                progressDiv.classList.add('hidden');
                progressFill.style.width = '0%';
                progressPercent.textContent = '0%';

                // Create download link
                const link = document.createElement('a');
                link.href = fileUrl;
                link.download = `${name}.mp3`;
                link.click();
            }, 500);
        }
    }, 200);
}

// Share functionality
async function sharePage(name, data) {
    const shareData = {
        title: `${name} | Vickerdent Studios`,
        text: `Download ${name} on Vickerdent Studios!`,
        url: data,
    };

    try {
        await navigator.share(shareData);
    } catch (err) {
        console.log(`Error: ${err}`);
    }
}
