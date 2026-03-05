from player_server.services.audio_os import AudioSystem

class AudioPlayer:
    def __init__(self):
        self.system = AudioSystem()
        self.current_track = None

    def play(self, file_path: str):
        self.current_track = file_path
        self.system.play(file_path)

    def stop(self):
        self.system.stop()
        self.current_track = None

player_instance = AudioPlayer()
