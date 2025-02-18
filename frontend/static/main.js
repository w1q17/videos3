async function login() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorElement = document.getElementById('error');
    
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });
        
        const data = await response.json();
        
        if (response.ok) {
            errorElement.textContent = '';
            showVideos(data);
        } else {
            errorElement.textContent = data.detail;
        }
    } catch (error) {
        errorElement.textContent = 'Ошибка подключения к серверу';
    }
}

function showVideos(data) {
    const videoContainer = document.getElementById('video-container');
    const bucketNameElement = document.getElementById('bucket-name');
    const videosElement = document.getElementById('videos');
    
    videoContainer.style.display = 'block';
    bucketNameElement.textContent = data.bucket_name;
    
    if (data.videos.length === 0) {
        videosElement.innerHTML = '<p>В бакете нет видеофайлов</p>';
        return;
    }
    
    const videoList = data.videos.map(video => `
        <div class="video-item">
            <div>Название: ${video.name}</div>
            <div>Размер: ${formatSize(video.size)}</div>
            <div>Последнее изменение: ${formatDate(video.last_modified)}</div>
        </div>
    `).join('');
    
    videosElement.innerHTML = videoList;
}

function formatSize(bytes) {
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    if (bytes === 0) return '0 Byte';
    const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
    return Math.round(bytes / Math.pow(1024, i), 2) + ' ' + sizes[i];
}

function formatDate(isoString) {
    return new Date(isoString).toLocaleString('ru-RU');
} 