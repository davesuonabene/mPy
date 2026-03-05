import miniaudio

class AudioSystem:
    def __init__(self):
        self.device = miniaudio.PlaybackDevice()
        self.stream = None
        self.is_playing = False

    def play(self, file_path: str):
        if self.is_playing:
            self.stop()
        try:
            self.stream = miniaudio.stream_file(file_path)
            self.device.start(self.stream)
            self.is_playing = True
        except Exception as e:
            print(f"Error playing file: {e}")
            self.is_playing = False

    def stop(self):
        if self.is_playing:
            self.device.stop()
            self.stream = None
            self.is_playing = False
