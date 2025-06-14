# app/config.py

SAMPLE_RATE = 44100         # Audio sample rate
BUFFER_SIZE = 2048          # Number of samples per buffer
FPS = 30                    # Frames per second for UI refresh
FFT_BINS = BUFFER_SIZE // 2 # Number of frequency bars to display
