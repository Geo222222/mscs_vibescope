import sounddevice as sd
import numpy as np
from config.config import SAMPLE_RATE, BUFFER_SIZE

class AudioInput:
    def __init__(self):
        """Initialize audio input stream"""
        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            blocksize=BUFFER_SIZE,
            # channels=1,
            dtype=np.float32
        )
        self.stream.start()

    def get_audio_chunk(self):
        """Capture and return a chunk of audio data"""
        try:
            audio_data, overflowed = self.stream.read(BUFFER_SIZE)
            audio_chunk = audio_data.flatten()
            
            # Add debug visualization
            level = np.abs(audio_chunk).mean()
            bars = int(level * 50)  # Scale for visualization
            print(f"Input Level: {'█' * bars}{' ' * (50-bars)} [{level:.4f}]", end='\r')
            
            return audio_chunk
        except Exception as e:
            print(f"🔴 Error capturing audio: {e}")
            return np.zeros(BUFFER_SIZE)

    def close(self):
        """Close the audio stream"""
        if hasattr(self, 'stream') and self.stream:
            self.stream.stop()
            self.stream.close()