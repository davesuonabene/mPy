import miniaudio
import array

class AudioSystem:
    def __init__(self):
        self.device = miniaudio.PlaybackDevice()
        self.stream = None
        self.is_playing = False
        self._volume = 1.0  # Initialize volume to 1.0 (full volume)
        self._is_muted = False
        # Do not use self.device.volume if it affects system volume
        self.device.volume = 1.0 
        self._current_pos = 0.0
        self._duration = 0.0
        self._sample_rate = 44100
        self._nchannels = 2
        self._current_file = None

    def set_volume(self, volume: float):
        if not 0.0 <= volume <= 1.0:
            raise ValueError("Volume must be between 0.0 and 1.0")
        self._volume = volume
        print(f"DEBUG: Internal volume set to {volume}")

    def get_volume(self) -> float:
        return self._volume

    def mute(self):
        if not self._is_muted:
            print("DEBUG: Internal mute")
            self._is_muted = True

    def unmute(self):
        if self._is_muted:
            print(f"DEBUG: Internal unmute (volume will be {self._volume})")
            self._is_muted = False


    def play(self, file_path: str, start_pos: float = 0.0):
        if self.is_playing:
            self.stop()
        try:
            file_info = miniaudio.get_file_info(file_path)
            self._duration = file_info.duration
            self._sample_rate = file_info.sample_rate
            self._nchannels = file_info.nchannels
            self._current_pos = start_pos
            self._current_file = file_path
            
            seek_frame = int(start_pos * self._sample_rate)
            
            # stream_file returns a generator of array.array('h')
            # SIGNED16 is default
            raw_stream = miniaudio.stream_file(file_path, seek_frame=seek_frame)
            
            def tracking_generator():
                try:
                    framecount = yield b"" 
                    while True:
                        try:
                            chunk = raw_stream.send(framecount)
                            
                            # Manual volume scaling
                            effective_vol = 0.0 if self._is_muted else self._volume
                            
                            if effective_vol != 1.0:
                                # Scale samples. chunk is array.array('h')
                                scaled_chunk = array.array('h', (int(v * effective_vol) for v in chunk))
                                output_data = scaled_chunk
                            else:
                                output_data = chunk

                            # In miniaudio, frames = total_samples // channels
                            # chunk is already an array of samples
                            frames = len(chunk) // self._nchannels
                            self._current_pos += frames / self._sample_rate
                            framecount = yield output_data
                        except StopIteration:
                            break
                finally:
                    self.is_playing = False

            self.stream = tracking_generator()
            next(self.stream) # Pre-start the generator
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
            self._current_pos = 0.0

    def seek(self, position: float):
        if self._current_file and 0 <= position <= self._duration:
            was_playing = self.is_playing
            self.play(self._current_file, start_pos=position)
            if not was_playing:
                self.stop()
                self._current_pos = position

    def get_current_position(self) -> float:
        return self._current_pos

    def get_duration(self) -> float:
        return self._duration
