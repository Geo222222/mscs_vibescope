from core.audio_input import AudioInput
from core.fft_processor import FFTProcessor
from ui.visualizer import Visualizer
from app.config import FPS
import pygame

def print_welcome():
    print("=" * 60)
    print("🎧  Welcome to VibeScope – Ambient Emotion Radar")
    print("📡  Listening for audio... analyzing frequency spectrum...")
    print("=" * 60)


def main():
    print_welcome()    
    audio = AudioInput()
    fft = FFTProcessor()
    ui = Visualizer()

    running = True
    while running:
        chunk = audio.get_audio_chunk()
        fft_data = fft.process(chunk)
        ui.draw(fft_data)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ui.clock.tick(FPS)

    ui.quit()

if __name__ == "__main__":
    main()

