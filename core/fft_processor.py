import numpy as np
from app.config import BUFFER_SIZE

class FFTProcessor:
    def process(self, audio_data):
        fft = np.abs(np.fft.rfft(audio_data))
        return fft / np.max(fft) if np.max(fft) != 0 else fft
