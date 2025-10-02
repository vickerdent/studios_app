
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const browseBtn = document.getElementById('browseBtn');
const uploadPrompt = document.getElementById('uploadPrompt');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const progressBar = document.getElementById('progressBar');
const uploadStatus = document.getElementById('uploadStatus');
const uploadBtn = document.getElementById('uploadBtn');
const cancelBtn = document.getElementById('cancelBtn');
const removeBtn = document.getElementById('removeBtn');
const uploadForm = document.getElementById("uploadForm");

const csrf = document.getElementsByName("csrfmiddlewaretoken");

let selectedFile = null;

// Browse button click
browseBtn.addEventListener('click', () => {
    fileInput.click();
});

// File input change
fileInput.addEventListener('change', (e) => {
    handleFile(e.target.files[0]);
});

// Drag and drop
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('drag-over');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    handleFile(e.dataTransfer.files[0]);
});

// Click to upload area
uploadArea.addEventListener('click', (e) => {
    if (e.target === uploadArea || e.target.closest('#uploadPrompt')) {
        fileInput.click();
    }
});

// Handle file selection
function handleFile(file) {
    if (!file) return;

    if (!file.type.startsWith('audio/')) {
        alert('Please select an audio file');
        return;
    }

    selectedFile = file;
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);

    uploadPrompt.classList.add('hidden');
    fileInfo.classList.remove('hidden');
    uploadBtn.disabled = false;
    uploadStatus.textContent = 'Ready to upload';
    progressBar.style.width = '0%';
}

// Remove file
removeBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    selectedFile = null;
    fileInput.value = '';
    uploadPrompt.classList.remove('hidden');
    fileInfo.classList.add('hidden');
    cancelBtn.classList.add("hidden")
    uploadBtn.disabled = true;
});

// Upload button
uploadBtn.addEventListener('click', (e) => {
    if (!selectedFile) return;

    e.preventDefault();
    e.stopPropagation();
    uploadBtn.disabled = true;
    removeBtn.disabled = true;
    uploadBtn.classList.add('uploading');
    cancelBtn.classList.remove("hidden")

    const formData = new FormData(uploadForm);
    formData.append("csrfmiddlewaretoken", csrf[0].value);
    formData.append("audio_file", selectedFile);
    console.log(selectedFile);

    $.ajax({
        type: 'POST',
        url: uploadForm.action,
        enctype: 'multipart/form-data',
        data: formData,
        beforeSend: function (params) {

        },
        xhr: function () {
            const xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener("progress", (e) => {
                // console.log(e);
                if (e.lengthComputable) {
                    const percent = e.loaded / e.total * 100;
                    console.log(percent)
                    progressBar.style.width = percent + '%';
                    uploadStatus.textContent = `Uploading: ${percent.toFixed(1)}%`;
                }
            })
            cancelBtn.addEventListener("click", () => {
                xhr.abort();
                progressBar.style.width = '0%';
                uploadStatus.textContent = 'Ready to upload';
                cancelBtn.classList.add("hidden");
                removeBtn.disabled = false;
                uploadBtn.disabled = false;
            })
            return xhr;
        },
        success: function (response) {
            console.log(response);
            uploadStatus.textContent = 'Upload complete!';
            uploadStatus.classList.add('text-green-400');
            uploadBtn.classList.remove('uploading');
            setTimeout(() => {
                // Show success message
                uploadArea.innerHTML = `
                    <div class="text-center py-8">
                        <div class="bg-green-600 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                        </div>
                        <h4 class="text-xl font-bold mb-2 text-green-400">Audio Uploaded Successfully!</h4>
                        <p class="text-gray-400 mb-6">The message is now ready for publishing</p>
                        <div class="flex gap-4 justify-center">
                            <button type="button" onclick="window.location.href='${response.redirect_url}'" class="bg-purple-600 hover:bg-purple-700 px-6 py-3 rounded-lg font-semibold transition-colors">
                                Back to Messages
                            </button>
                        </div>
                    </div>
                `;
                cancelBtn.classList.add("hidden")
            }, 500);
        },
        error: function (error) {
            console.log(error);
            uploadArea.innerHTML = `
                <div class="text-center py-8">
                    <div class="bg-red-600 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="w-8 h-8 text-white" viewBox="0 0 16 16">
                            <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>
                            <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/>
                        </svg>
                    </div>
                    <h4 class="text-xl font-bold mb-2 text-red-400">An Error occurred!</h4>
                    <p class="text-gray-400 mb-6">Reload the page to try again</p>
                </div>
            `;
        },
        cache: false,
        contentType: false,
        processData: false
    })
});

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}
