document.addEventListener("DOMContentLoaded", () => {

    registerServiceWorker()

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


// Utils functions:

function urlBase64ToUint8Array (base64String) {
  var padding = '='.repeat((4 - base64String.length % 4) % 4)
  var base64 = (base64String + padding)
    .replace(/\-/g, '+')
    .replace(/_/g, '/')

  var rawData = window.atob(base64)
  var outputArray = new Uint8Array(rawData.length)

  for (var i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i)
  }
  return outputArray;
}

var applicationServerKey = "BG6Q0IHbtSWC1RfQex3shIhH2S3LSLl6YEi568Cq4jZg1KT55jRMz6e32y7Qqh-cvqMkGfMth6K2qjlzguPwOGU";

// Register the service worker first
async function registerServiceWorker() {
  if ('serviceWorker' in navigator) {
    // Register from root path with root scope so it can control the entire site
    try {
        const registration = await navigator.serviceWorker.register('/sw.js', { scope: '/' });
        console.log('Service Worker registered successfully!');
        console.log('Scope:', registration.scope);
        return registration;
      } catch (error) {
        console.error('Service Worker registration failed:', error);
        throw error;
      }
  }
  return Promise.reject('Service Worker not supported');
}

function subscribeUser() {
  if ('Notification' in window && 'serviceWorker' in navigator) {
    // Wait for service worker to be ready
    navigator.serviceWorker.ready.then(function (reg) {
        console.log("Service Worker is ready, now subscribing...");
        console.log(reg);

      reg.pushManager
        .subscribe({
          userVisibleOnly: true,
          applicationServerKey: urlBase64ToUint8Array(
            applicationServerKey
          ),
        })
        .then(function (sub) {
            console.log(sub.endpoint);

          var registration_id = sub.endpoint;
          var data = {
            p256dh: btoa(
              String.fromCharCode.apply(
                null,
                new Uint8Array(sub.getKey('p256dh'))
              )
            ),
            auth: btoa(
              String.fromCharCode.apply(
                null,
                new Uint8Array(sub.getKey('auth'))
              )
            ),
            registration_id: registration_id,
            group: "message_requests"
          }

          requestPOSTToServer(data)
        })
        .catch(function (e) {
            console.log("Error subscribing to push:", e);
          if (Notification.permission === 'denied') {
            console.warn('Permission for notifications was denied');
            document.getElementById("toast-danger").classList.remove("hidden");
            document.getElementById("toast-danger").classList.add("flex");
          } else {
            console.error('Unable to subscribe to push', e);
            // Show error toast for other errors
            document.getElementById("toast-danger").classList.remove("hidden");
            document.getElementById("toast-danger").classList.add("flex");
          }
        })
    }).catch(function(error) {
      console.error('Service Worker not ready:', error);
      // Try registering the service worker again
      registerServiceWorker().then(function() {
        console.log('Retrying subscription after registration...');
        // Retry subscription after a short delay
        setTimeout(function() {
          subscribeUser();
        }, 1000);
      }).catch(function(err) {
        console.error('Failed to register service worker:', err);
        document.getElementById("toast-danger").classList.remove("hidden");
        document.getElementById("toast-danger").classList.add("flex");
      });
    });
  }
}

// Send the subscription data to your server
async function requestPOSTToServer (data) {
  const headers = new Headers();
  const csrftoken = getCookie("csrftoken");
  headers.set('Content-Type', 'application/json');
  headers.set('X-CSRFToken', csrftoken)
  const requestOptions = {
    method: 'POST',
    headers,
    mode: "same-origin",
    body: JSON.stringify(data),
  };

  return (
    fetch('/notifications/register/', requestOptions)
    .then((response) => {
        if (!response.ok) {
            failToast.show();
            throw new Error(
                `HTTP error! Status: ${response.status}`
            );
        }
        return response.json();
    }).then((data) => {
        const result = data.result;
        if (result) {
            // Successful process
            const bannerButton = document.getElementById("close-banner");
            bannerButton.click();
            document.getElementById("toast-success").classList.remove("hidden");
            document.getElementById("toast-success").classList.add("flex");
        }
    }) .catch((error) => {
        document.getElementById("toast-danger").classList.remove("hidden");
        document.getElementById("toast-danger").classList.add("flex");
        console.error({ error: error });
    })
)}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
