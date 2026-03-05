let tracks = [];
let selectedIndex = -1;
let currentVolume = 1.0; // Keep track of the current volume, initialized to 1.0

const volumeSlider = document.getElementById('volumeSlider');
const muteBtn = document.getElementById('muteBtn');
const volumeDisplay = document.getElementById('volumeDisplay');
const currentlyPlayingDiv = document.getElementById('currentlyPlaying');
const errorDisplay = document.createElement('div'); // Create a div for error messages
errorDisplay.id = 'errorDisplay';
errorDisplay.style.color = 'red';
errorDisplay.style.marginTop = '10px';
document.getElementById('app').prepend(errorDisplay); // Add it to the top of the app div

function displayError(message) {
    errorDisplay.textContent = `Error: ${message}`;
    console.error(message);
}

function clearError() {
    errorDisplay.textContent = '';
}

async function safeFetch(url, options) {
    clearError();
    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            let errorData = {};
            try {
                errorData = await response.json();
            } catch (jsonError) {
                // If response is not JSON, use the plain text
                const text = await response.text();
                displayError(`HTTP error! status: ${response.status}. Response: ${text.substring(0, 200)}`);
                return null;
            }
            displayError(errorData.detail || `HTTP error! status: ${response.status}.`);
            return null;
        }
        return response.json();
    } catch (error) {
        displayError(`Network error or failed to parse response: ${error.message}`);
        return null;
    }
}

async function loadTracks() {
    const data = await safeFetch('/api/v1/tracks');
    if (data) {
        tracks = data;
        renderTrackList();
    }
}

function renderTrackList() {
    const list = document.getElementById('trackList');
    list.innerHTML = '';

    tracks.forEach((track, index) => {
        const li = document.createElement('li');
        li.textContent = track.title || track.filename || 'Unknown Track';
        li.className = 'track-item';
        if (index === selectedIndex) {
            li.classList.add('selected');
        }
        li.onclick = () => {
            selectTrack(index);
        };
        list.appendChild(li);
    });
}

function getSelectedTrack() {
    return tracks[selectedIndex];
}

function updateVolumeDisplay(volume) {
    currentVolume = volume;
    volumeSlider.value = volume;
    volumeDisplay.textContent = `${Math.round(volume * 100)}%`;
    muteBtn.textContent = volume === 0 ? 'Unmute' : 'Mute';
    console.log(`Volume displayed: ${volume}`); // LOG
}

async function fetchAndSetInitialVolume() {
    console.log('Fetching initial volume...'); // LOG
    const data = await safeFetch('/api/v1/volume');
    if (data && typeof data.volume === 'number') {
        updateVolumeDisplay(data.volume);
    } else {
        console.error('Failed to fetch initial volume or invalid data:', data); // LOG
    }
}

async function setVolume(volume) {
    console.log('Setting volume to:', volume); // LOG
    const data = await safeFetch('/api/v1/volume', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ volume: parseFloat(volume) })
    });
    if (data && data.status === 'volume set') {
        updateVolumeDisplay(data.volume);
    } else {
        console.error('Failed to set volume or invalid data:', data); // LOG
    }
}

async function toggleMute() {
    if (muteBtn.textContent === 'Mute') {
        console.log('Muting audio...'); // LOG
        const data = await safeFetch('/api/v1/mute', { method: 'POST' });
        if (data && data.status === 'muted') {
            updateVolumeDisplay(0); // Assuming mute sets volume to 0
        } else {
            console.error('Failed to mute audio or invalid data:', data); // LOG
        }
    } else {
        console.log('Unmuting audio...'); // LOG
        const data = await safeFetch('/api/v1/unmute', { method: 'POST' });
        if (data && data.status === 'unmuted') {
            await fetchAndSetInitialVolume();
        } else {
            console.error('Failed to unmute audio or invalid data:', data); // LOG
        }
    }
}

async function playSelectedTrack() {
    const track = getSelectedTrack();
    if (!track) {
        displayError('No track selected.');
        return;
    }
    const title = track.title || track.filename;
    if (title) {
        const data = await safeFetch('/api/v1/play', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ file_path: track.file_path })
        });
        if (data && data.status === 'playing') {
            currentlyPlayingDiv.textContent = `Currently playing: ${title}`;
        } else {
            console.error('Failed to play track or invalid data:', data); // LOG
        }
    }
}

document.getElementById('playBtn').onclick = async () => {
    playSelectedTrack();
};

document.getElementById('stopBtn').onclick = async () => {
    console.log('Stopping track...'); // LOG
    const data = await safeFetch('/api/v1/stop', { method: 'POST' });
    if (data && data.status === 'stopped') {
        currentlyPlayingDiv.textContent = 'here there is just silence';
    } else {
        console.error('Failed to stop track or invalid data:', data); // LOG
    }
};

document.getElementById('prevBtn').onclick = async () => {
    if (tracks.length === 0) {
        displayError('No tracks available.');
        return;
    }
    let newIndex = selectedIndex - 1;
    if (newIndex < 0) {
        newIndex = tracks.length - 1; // Wrap around
    }
    selectTrack(newIndex);
};

document.getElementById('nextBtn').onclick = async () => {
    if (tracks.length === 0) {
        displayError('No tracks available.');
        return;
    }
    let newIndex = selectedIndex + 1;
    if (newIndex >= tracks.length) {
        newIndex = 0; // Wrap around
    }
    selectTrack(newIndex);
};

function selectTrack(index) {
    if (index < 0 || index >= tracks.length) return;
    selectedIndex = index;
    renderTrackList();
    playSelectedTrack();
}

let isSeeking = false;
const progressBar = document.getElementById('progressBar');

function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
}

async function updateTransportBar() {
    console.log('Updating transport bar...'); // LOG
    const status = await safeFetch('/api/v1/status');
    if (!status) {
        console.error('Failed to get status for transport bar update.'); // LOG
        return;
    }

    const currentTimeSpan = document.getElementById('currentTime');
    const durationSpan = document.getElementById('duration');

    if (!isSeeking) {
        currentTimeSpan.textContent = formatTime(status.current_position);
        if (status.duration > 0) {
            durationSpan.textContent = formatTime(status.duration);
            progressBar.max = Math.floor(status.duration);
            progressBar.value = Math.floor(status.current_position);
        } else {
            durationSpan.textContent = '0:00';
            progressBar.max = 100;
            progressBar.value = 0;
        }
    }

    if (status.is_playing && status.current_track_title) {
        currentlyPlayingDiv.textContent = `Currently playing: ${status.current_track_title}`;
    } else if (!status.is_playing && currentlyPlayingDiv.textContent !== 'here there is just silence') {
        currentlyPlayingDiv.textContent = 'here there is just silence';
    }
    console.log('Transport bar updated with status:', status); // LOG
}

progressBar.addEventListener('input', () => {
    isSeeking = true;
    document.getElementById('currentTime').textContent = formatTime(progressBar.value);
});

progressBar.addEventListener('change', async () => {
    const newPosition = parseFloat(progressBar.value);
    console.log('Seeking to:', newPosition);
    await safeFetch('/api/v1/seek', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ position: newPosition })
    });
    isSeeking = false;
});

setInterval(updateTransportBar, 1000);

volumeSlider.addEventListener('input', (event) => {
    updateVolumeDisplay(parseFloat(event.target.value));
});

volumeSlider.addEventListener('change', (event) => {
    setVolume(event.target.value);
});

muteBtn.addEventListener('click', toggleMute);

window.onload = () => {
    loadTracks();
    fetchAndSetInitialVolume();
};
