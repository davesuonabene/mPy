import miniaudio
import time

def test_play():
    stream = miniaudio.stream_file("data/music/12 Cold War (Instrumental).mp3")
    device = miniaudio.PlaybackDevice()
    device.start(stream)
    print("Playing...")
    time.sleep(2)
    device.stop()
    print("Stopped.")

if __name__ == "__main__":
    test_play()
