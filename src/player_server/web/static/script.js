let tracks = [];
let selectedIndex = -1;

async function loadTracks() {
    try {
        const response = await fetch('/api/v1/tracks');
        tracks = await response.json();
        renderTrackList();
    } catch (error) {
        console.error('Failed to fetch tracks:', error);
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

function selectTrack(index) {
    if (index < 0 || index >= tracks.length) return;
    selectedIndex = index;
    renderTrackList();
}

function getSelectedTrack() {
    return tracks[selectedIndex];
}

document.getElementById('playBtn').onclick = async () => {
    const track = getSelectedTrack();
    if (!track) return;
    const title = track.title || track.filename;
    if (title) {
        document.getElementById('currentlyPlaying').textContent = `Currently playing: ${title}`;
        await fetch('/api/v1/play', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ file_path: track.file_path })
        });
    }
};

document.getElementById('stopBtn').onclick = async () => {
    document.getElementById('currentlyPlaying').textContent = 'here there is just silence';
    await fetch('/api/v1/stop', { method: 'POST' });
};

document.getElementById('prevBtn').onclick = async () => {
    if (tracks.length === 0) return;
    let newIndex = selectedIndex - 1;
    if (newIndex < 0) {
        newIndex = tracks.length - 1; // Wrap around
    }
    selectTrack(newIndex);
    const track = getSelectedTrack();
    const title = track ? (track.title || track.filename) : null;
    if (title) {
        document.getElementById('currentlyPlaying').textContent = `Currently playing: ${title}`;
        await fetch('/api/v1/play', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ file_path: track.file_path })
        });
    }
};

document.getElementById('nextBtn').onclick = async () => {
    if (tracks.length === 0) return;
    let newIndex = selectedIndex + 1;
    if (newIndex >= tracks.length) {
        newIndex = 0; // Wrap around
    }
    selectTrack(newIndex);
    const track = getSelectedTrack();
    const title = track ? (track.title || track.filename) : null;
    if (title) {
        document.getElementById('currentlyPlaying').textContent = `Currently playing: ${title}`;
        await fetch('/api/v1/play', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ file_path: track.file_path })
        });
    }
};

window.onload = loadTracks;
