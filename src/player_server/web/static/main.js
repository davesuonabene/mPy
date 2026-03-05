document.addEventListener('DOMContentLoaded', () => {
    const playPauseBtn = document.getElementById('play-pause');
    const nowPlaying = document.getElementById('now-playing');
    let isPlaying = false;

    playPauseBtn.addEventListener('click', () => {
        isPlaying = !isPlaying;
        playPauseBtn.textContent = isPlaying ? 'Pause' : 'Play';
        if (isPlaying) {
            console.log('Resume playback');
        } else {
            console.log('Pause playback');
        }
    });

    document.querySelectorAll('.play-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const trackItem = e.target.closest('.track-item');
            const title = trackItem.querySelector('.track-title').textContent;
            const artist = trackItem.querySelector('.track-artist').textContent;
            nowPlaying.textContent = `Playing: ${title} - ${artist}`;
            isPlaying = true;
            playPauseBtn.textContent = 'Pause';
            console.log(`Starting track: ${title}`);
        });
    });
});
