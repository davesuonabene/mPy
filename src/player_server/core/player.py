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

    def get_current_position(self) -> float:
        return self.system.get_current_position()

    def get_duration(self) -> float:
        return self.system.get_duration()

    def set_volume(self, volume: float):
        self.system.set_volume(volume)

    def get_volume(self) -> float:
        return self.system.get_volume()

    def mute(self):
        self.system.mute()

    def unmute(self):
        self.system.unmute()

    def seek(self, position: float):
        self.system.seek(position)

player_instance = AudioPlayer()
